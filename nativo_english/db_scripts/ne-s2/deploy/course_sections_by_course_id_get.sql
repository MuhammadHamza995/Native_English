/*****************************************************
Author: Hadiya Kashif
Ticket: https://app.clickup.com/t/868axzz4x
Description: This function will return all sections of a course by course id

Params: course_id
*****************************************************/

-- Drop the function if it already exists
DROP FUNCTION IF EXISTS course_section_by_course_id_get(BIGINT);

-- Create or replace the function
CREATE OR REPLACE FUNCTION course_section_by_course_id_get(p_course_id BIGINT)
RETURNS TABLE(
    section_id BIGINT,
    section_title VARCHAR,
    section_description TEXT,
    fk_course_id BIGINT,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ
) AS
$$
BEGIN
    RETURN QUERY
    SELECT 
        cs.id AS section_id,
        cs.section_title,
        cs.section_description,
        cs.fk_course_id,
        cs.created_at,
        cs.updated_at
    FROM course_coursesection cs
    WHERE cs.fk_course_id = p_course_id;
END;
$$ LANGUAGE plpgsql;
