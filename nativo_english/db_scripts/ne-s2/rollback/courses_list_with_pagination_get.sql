/*****************************************************
Author: Muhammad Hassaan Bashir
Ticket: 
Description: Rollback of function courses_list_with_pagination_get
*****************************************************/

-- Drop the function if it already exists
DROP FUNCTION IF EXISTS courses_list_with_pagination_get(INT, INT, TEXT, TEXT, BOOLEAN, TEXT, TEXT, TEXT);