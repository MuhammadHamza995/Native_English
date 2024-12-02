/*****************************************************
Author: Hadiya Kashif
Ticket: https://app.clickup.com/t/868axzz4x
Description: This function will return course details by course ID, including the enrollment count.

Params: course_id, owner_id (optional for teacher role)
*****************************************************/

-- Drop the function if it already exists
DROP FUNCTION IF EXISTS course_detail_by_id_get(INT);
DROP FUNCTION IF EXISTS course_detail_by_id_get(INT, BIGINT);

-- Create or replace the function
CREATE OR REPLACE FUNCTION course_detail_by_id_get(
    p_course_id INT,          -- Course ID
    p_owner_id BIGINT DEFAULT NULL -- Owner ID (optional, for teacher role)
)
RETURNS TABLE(
    course_id BIGINT,
    title VARCHAR,
    description TEXT,
    is_paid BOOLEAN,
    price FLOAT,
    mode VARCHAR,
    avg_rating FLOAT,
    is_active BOOLEAN,
    enrollment_count BIGINT,
    created_at TIMESTAMPTZ,
    created_by_name TEXT,
    updated_at TIMESTAMPTZ,
    updated_by_name TEXT,
    owner_name TEXT
) AS
$$
BEGIN
    RETURN QUERY
    SELECT 
        crs.id AS course_id,
        crs.title,
        crs.description,
        crs.is_paid,
        crs.price,
        crs.mode,
        crs.avg_rating,
        crs.is_active,
        COALESCE(COUNT(ce.id), 0) AS enrollment_count, -- Count of enrollments
        crs.created_at,
        COALESCE(
            CASE 
                WHEN creator.first_name IS NOT NULL OR creator.last_name IS NOT NULL 
                THEN CONCAT(
                    COALESCE(creator.first_name, ''), 
                    CASE WHEN creator.first_name IS NOT NULL AND creator.last_name IS NOT NULL THEN ' ' ELSE '' END,
                    COALESCE(creator.last_name, '')
                )
                ELSE ''
            END,
            ''
        ) AS created_by_name, -- Created by name
        crs.updated_at,
        COALESCE(
            CASE 
                WHEN updater.first_name IS NOT NULL OR updater.last_name IS NOT NULL 
                THEN CONCAT(
                    COALESCE(updater.first_name, ''), 
                    CASE WHEN updater.first_name IS NOT NULL AND updater.last_name IS NOT NULL THEN ' ' ELSE '' END,
                    COALESCE(updater.last_name, '')
                )
                ELSE ''
            END,
            ''
        ) AS updated_by_name, -- Updated by name
        COALESCE(
            CASE 
                WHEN owner.first_name IS NOT NULL OR owner.last_name IS NOT NULL 
                THEN CONCAT(
                    COALESCE(owner.first_name, ''), 
                    CASE WHEN owner.first_name IS NOT NULL AND owner.last_name IS NOT NULL THEN ' ' ELSE '' END,
                    COALESCE(owner.last_name, '')
                )
                ELSE ''
            END,
            ''
        ) AS owner_name -- Owner name
    FROM 
        "course_course" crs
    LEFT JOIN 
        "course_courseenrollment" ce ON crs.id = ce.fk_course_id AND ce.is_active = TRUE
    LEFT JOIN 
        "User_user" creator ON crs.created_by = creator.id
    LEFT JOIN 
        "User_user" updater ON crs.modified_by = updater.id
    LEFT JOIN 
        "User_user" owner ON crs.fk_owner_id = owner.id
    WHERE 
        crs.id = p_course_id
        AND (p_owner_id IS NULL OR crs.fk_owner_id = p_owner_id) -- Filter by owner if provided
    GROUP BY 
        crs.id, creator.first_name, creator.last_name, updater.first_name, updater.last_name, owner.first_name, owner.last_name;
END;
$$ LANGUAGE plpgsql;
