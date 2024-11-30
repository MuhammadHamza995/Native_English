/*****************************************************
Author: Hadiya Kashif
Ticket: https://app.clickup.com/t/868axzz4x
Description: roll back of course_detail_by_id_get

Params: course_id
*****************************************************/

-- Drop the function if it already exists
DROP FUNCTION IF EXISTS course_detail_by_id_get(INT);
