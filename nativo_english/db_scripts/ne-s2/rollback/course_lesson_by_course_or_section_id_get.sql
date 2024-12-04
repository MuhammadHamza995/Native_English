/*****************************************************
Author: Hadiya Kashif
Ticket: https://app.clickup.com/t/868axzz4x
Description: This function will return course lesson details by course ID or section ID

Params: course_id, section_id
*****************************************************/

-- Drop the function if it already exists
DROP FUNCTION IF EXISTS course_lesson_by_course_or_section_id_get(INT,INT);

