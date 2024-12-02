/*****************************************************
Author: Muhammad Hassaan Bashir
Ticket: 
Description: This function will return all courses with sorting and filtering options, including owner-specific filtering and the updated by user name.
*****************************************************/

-- Drop the function if it already exists
DROP FUNCTION IF EXISTS courses_list_with_pagination_get(INT, INT, TEXT, TEXT, BOOLEAN, BOOLEAN, TEXT, TEXT, TEXT, BIGINT);

-- Create or replace the function
CREATE OR REPLACE FUNCTION courses_list_with_pagination_get(
    page_num INT DEFAULT 1,
    page_size INT DEFAULT 10,
    filter_title TEXT DEFAULT NULL,
    filter_mode TEXT DEFAULT NULL,
    filter_is_paid BOOLEAN DEFAULT NULL,
    filter_is_active BOOLEAN DEFAULT TRUE,
    search_query TEXT DEFAULT NULL,
    sort_field TEXT DEFAULT 'created_at',  -- Default sort by creation date
    sort_direction TEXT DEFAULT 'DESC',   -- Default sort direction is descending
    filter_owner_id BIGINT DEFAULT NULL   -- Filter by owner ID
)

RETURNS TABLE (
    course_id BIGINT,
    title character varying,
    description TEXT,
    is_paid BOOLEAN,
    price FLOAT,
    mode character varying,
    avg_rating FLOAT,
    is_active BOOLEAN,
    owner_name TEXT,
    updated_by_name TEXT,
    owner BIGINT,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ,
    enrollment_count BIGINT,
    total_count BIGINT
) AS $$
DECLARE
    total_courses BIGINT;
BEGIN

    -- Get the total count of matching courses
    SELECT COUNT(*) INTO total_courses
    FROM course_course c
    LEFT JOIN course_courseenrollment ce ON c.id = ce.fk_course_id
    WHERE c.is_active = filter_is_active
    AND (filter_title IS NULL OR c.title ILIKE '%' || filter_title || '%')
    AND (filter_mode IS NULL OR c.mode ILIKE '%' || filter_mode || '%')
    AND (filter_is_paid IS NULL OR c.is_paid = filter_is_paid)
    AND (filter_owner_id IS NULL OR c.fk_owner_id = filter_owner_id)
    AND (
        search_query IS NULL
        OR c.title ILIKE '%' || search_query || '%'
        OR c.description ILIKE '%' || search_query || '%'
    );

    -- Return the paginated courses along with the total count
    RETURN QUERY
    SELECT
        c.id AS course_id,
        c.title,
        c.description,
        c.is_paid,
        c.price,
        c.mode,
        c.avg_rating,
        c.is_active,
        COALESCE(
		    CASE 
		        WHEN owner_user.first_name IS NOT NULL OR owner_user.last_name IS NOT NULL 
				THEN CONCAT(
					COALESCE(owner_user.first_name, ''),
					CASE WHEN owner_user.first_name IS NOT NULL AND owner_user.last_name IS NOT NULL THEN ' ' ELSE '' END,
		            COALESCE(owner_user.last_name, '')
				)   
		        ELSE 'NA'
		    END,
		    'NA'
		) AS owner_name,
        COALESCE(
		    CASE 
		        WHEN updated_user.first_name IS NOT NULL OR updated_user.last_name IS NOT NULL 
		        THEN CONCAT(
		    		COALESCE(updated_user.first_name, ''), 
					CASE WHEN updated_user.first_name IS NOT NULL AND updated_user.last_name IS NOT NULL THEN ' ' ELSE '' END,
		            COALESCE(updated_user.last_name, '')
		        )
		        ELSE ''
		    END,
		    ''
		) AS updated_by_name,
        c.fk_owner_id AS owner,
        c.created_at,
        c.updated_at,
        COALESCE(COUNT(ce.id), 0) AS enrollment_count,
        total_courses AS total_count  -- Return the total courses count in each row
    FROM
        course_course c
    LEFT JOIN
        "User_user" owner_user ON c.fk_owner_id = owner_user.id
    LEFT JOIN
        "User_user" updated_user ON c.modified_by = updated_user.id
    LEFT JOIN
        course_courseenrollment ce ON c.id = ce.fk_course_id
    WHERE
        c.is_active = filter_is_active
        AND (filter_title IS NULL OR c.title ILIKE '%' || filter_title || '%')
        AND (filter_mode IS NULL OR c.mode ILIKE '%' || filter_mode || '%')
        AND (filter_is_paid IS NULL OR c.is_paid = filter_is_paid)
        AND (filter_owner_id IS NULL OR c.fk_owner_id = filter_owner_id)
        AND (
            search_query IS NULL
            OR c.title ILIKE '%' || search_query || '%'
            OR c.description ILIKE '%' || search_query || '%'
        )
    GROUP BY
        c.id, owner_user.first_name, owner_user.last_name, updated_user.first_name, updated_user.last_name
    ORDER BY
        CASE WHEN sort_direction = 'ASC' AND sort_field = 'course_id' THEN c.id END ASC,
        CASE WHEN sort_direction = 'DESC' AND sort_field = 'course_id' THEN c.id END DESC,
        CASE WHEN sort_direction = 'ASC' AND sort_field = 'title' THEN c.title END ASC,
        CASE WHEN sort_direction = 'DESC' AND sort_field = 'title' THEN c.title END DESC,
        CASE WHEN sort_direction = 'ASC' AND sort_field = 'price' THEN c.price END ASC,
        CASE WHEN sort_direction = 'DESC' AND sort_field = 'price' THEN c.price END DESC,
        CASE WHEN sort_direction = 'ASC' AND sort_field = 'avg_rating' THEN c.avg_rating END ASC,
        CASE WHEN sort_direction = 'DESC' AND sort_field = 'avg_rating' THEN c.avg_rating END DESC,
        CASE WHEN sort_direction = 'ASC' AND sort_field = 'created_at' THEN c.created_at END ASC,
        CASE WHEN sort_direction = 'DESC' AND sort_field = 'created_at' THEN c.created_at END DESC,
        CASE WHEN sort_direction = 'ASC' AND sort_field = 'updated_at' THEN c.updated_at END ASC,
        CASE WHEN sort_direction = 'DESC' AND sort_field = 'updated_at' THEN c.updated_at END DESC,
        CASE WHEN sort_direction = 'ASC' AND sort_field = 'enrollment_count' THEN COUNT(ce.id) END ASC,
        CASE WHEN sort_direction = 'DESC' AND sort_field = 'enrollment_count' THEN COUNT(ce.id) END DESC,
        CASE WHEN (sort_direction = '' OR sort_direction IS NULL) AND (sort_field = '' OR sort_field IS NULL) THEN c.created_at END DESC
    LIMIT page_size OFFSET (page_num - 1) * page_size;

END;

$$ LANGUAGE plpgsql;
