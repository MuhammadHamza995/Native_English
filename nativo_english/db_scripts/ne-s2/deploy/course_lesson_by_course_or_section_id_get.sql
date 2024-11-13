/*****************************************************
Author: Hadiya Kashif
Ticket: https://app.clickup.com/t/868axzz4x
Description: This function will return course lesson details by course ID or section ID

Params: course_id, section_id
*****************************************************/

-- Drop the function if it already exists
DROP FUNCTION IF EXISTS course_lesson_by_course_or_section_id_get(INT,INT);

-- Create or replace the function to return course details
CREATE OR REPLACE FUNCTION course_lesson_by_course_or_section_id_get(p_course_id INT, p_section_id INT)
RETURNS TABLE(
    lesson_id BIGINT,
    lesson_title VARCHAR,
    lesson_description TEXT,
    lesson_position INT,
    section_id BIGINT,
    course_id BIGINT,
    is_active BOOLEAN
) AS
$$
BEGIN
    RETURN QUERY
    SELECT 
        lsn.id AS lesson_id,
        lsn.lesson_title,
        lsn.lesson_description,
        lsn.lesson_position,
        lsn.fk_section_id AS section_id,
        sec.fk_course_id AS course_id,
        lsn.is_active
    FROM "course_courselesson" lsn
    INNER JOIN "course_coursesection" sec ON sec.id = lsn.fk_section_id
    WHERE (p_course_id IS NULL OR sec.fk_course_id = p_course_id)
      AND (p_section_id IS NULL OR lsn.fk_section_id = p_section_id)
      AND lsn.is_active = TRUE;
END;
$$ LANGUAGE plpgsql;
