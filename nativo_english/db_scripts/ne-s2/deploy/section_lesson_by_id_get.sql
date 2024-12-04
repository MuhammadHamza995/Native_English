/*****************************************************
Author: Hadiya Kashif
Ticket: https://app.clickup.com/t/868axzz4x
Description: This function will return lesson details for a section by lesson ID

Params: lesson_id
*****************************************************/

-- Drop the function if it already exists
DROP FUNCTION IF EXISTS course_lesson_detail_by_id_get(INT);

-- Create or replace the function to return course lesson details
CREATE OR REPLACE FUNCTION course_lesson_detail_by_id_get(p_lesson_id INT)
RETURNS TABLE(
    lesson_id BIGINT,
    lesson_title VARCHAR,
    lesson_description TEXT,
    lesson_position INT,
    fk_section_id BIGINT,
    is_active BOOLEAN
) AS
$$
BEGIN
    RETURN QUERY
    SELECT 
        les.id AS lesson_id,
        les.lesson_title,
        les.lesson_description,
        les.lesson_position,
        les.fk_section_id,
        les.is_active
    FROM "course_courselesson" les
    WHERE les.id = p_lesson_id;
END;
$$ LANGUAGE plpgsql;
