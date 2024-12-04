/*****************************************************
Author: Hadiya Kashif
Ticket: https://app.clickup.com/t/868axzz4x
Description: roll back of course_section_by_course_id_get

Params: course_id
*****************************************************/

-- Drop the function if it already exists
DROP FUNCTION IF EXISTS course_section_by_course_id_get(BIGINT);
