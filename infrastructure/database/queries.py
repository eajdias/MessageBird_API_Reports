# SQL Queries for Standalone Report Generator

AGENT_MSG_CNVS_QUERY = """
    SELECT
        cv.cnvs_id,
        cv.cnvs_created,
        cv.cnvs_dept,
        cv.cnvs_contact_reason,
        cv.cnvs_rating_nps,
        cv.cnvs_occurrence,
        c.cnts_name,
        c.cnts_phone,
        m.msgs_created,
        m.msgs_direction,
        a.agnt_name
    FROM conversations cv
    JOIN contacts c ON cv.cnvs_cnts = c.cnts_id
    JOIN messages m ON cv.cnvs_id = m.msgs_cnvs
    LEFT JOIN agents a ON m.msgs_agnt = a.agnt_id
    WHERE datetime(cv.cnvs_created) BETWEEN ? AND ?
    ORDER BY cv.cnvs_id, m.msgs_created ASC
"""

SURVEY_DATA_METADATA_QUERY = """
    SELECT
        a.agnt_name,
        c.cnts_name,
        c.cnts_phone,
        cv.cnvs_id,
        cv.cnvs_created,
        cv.cnvs_updated,
        cv.cnvs_status,
        cv.cnvs_lang,
        cv.cnvs_software,
        cv.cnvs_tax_id,
        cv.cnvs_dept,
        cv.cnvs_rating_agent,
        cv.cnvs_rating_nps,
        cv.cnvs_contact_reason,
        cv.cnvs_occurrence,
        m.msgs_id,
        m.msgs_created,
        m.msgs_direction,
        m.msgs_agnt,
        qt.queue_time
    FROM messages m
    JOIN agents a ON m.msgs_agnt = a.agnt_id
    JOIN conversations cv ON m.msgs_cnvs = cv.cnvs_id
    JOIN contacts c ON cv.cnvs_cnts = c.cnts_id
    LEFT JOIN (
        SELECT m2.msgs_cnvs, MAX(m2.msgs_created) as queue_time
        FROM messages m2
        JOIN (
            SELECT msgs_cnvs, MIN(msgs_created) as first_agent_msg
            FROM messages
            WHERE msgs_agnt IS NOT NULL AND msgs_direction = 'sent'
            GROUP BY msgs_cnvs
        ) fa ON fa.msgs_cnvs = m2.msgs_cnvs
        WHERE m2.msgs_direction = 'received' AND m2.msgs_created <= fa.first_agent_msg
        GROUP BY m2.msgs_cnvs
    ) qt ON qt.msgs_cnvs = cv.cnvs_id
    WHERE datetime(cv.cnvs_created) BETWEEN ? AND ?
    ORDER BY cv.cnvs_id, m.msgs_created ASC
"""

ALL_MSGS_RANGE_QUERY = """
    SELECT
        m.msgs_created,
        m.msgs_cnvs,
        m.msgs_content,
        m.msgs_direction,
        a.agnt_name,
        c.cnts_name,
        cv.cnvs_id
    FROM messages m
    JOIN conversations cv ON m.msgs_cnvs = cv.cnvs_id
    JOIN contacts c ON cv.cnvs_cnts = c.cnts_id
    LEFT JOIN agents a ON m.msgs_agnt = a.agnt_id
    WHERE datetime(m.msgs_created) BETWEEN ? AND ?
    ORDER BY m.msgs_created ASC
"""

OS_DATA_QUERY = """
SELECT
    c.cnvs_id,
    c.cnvs_bird,
    c.cnvs_agnt,
    c.cnvs_msgcount,
    c.cnvs_created,
    c.cnvs_updated,
    c.cnvs_dept,
    c.cnvs_contact_reason,
    c.cnvs_occurrence,
    c.cnvs_software,
    c.cnvs_rating_agent,
    c.cnvs_rating_nps,
    c.cnvs_reopened_count,
    c.cnvs_description,
    ct.cnts_id,
    ct.cnts_name,
    ct.cnts_phone,
    ct.cnts_custom1,
    ct.cnts_custom2,
    ct.cnts_custom3,
    ct.cnts_custom4,
    a.agnt_name,
    ROUND((julianday(c.cnvs_updated) - julianday(c.cnvs_created)) * 1440) as calc_duration_min
FROM conversations c
LEFT JOIN contacts ct ON ct.cnts_id = c.cnvs_cnts
LEFT JOIN agents a ON a.agnt_id = c.cnvs_agnt
WHERE c.cnvs_created >= ?
  AND c.cnvs_created <= ?
ORDER BY c.cnvs_created
"""

UNMAPPED_AGENTS_QUERY = "SELECT COUNT(*) FROM conversations WHERE cnvs_agnt IS NOT NULL AND cnvs_agnt NOT IN (SELECT agnt_id FROM agents)"
UNMAPPED_DEPTS_QUERY = "SELECT COUNT(*) FROM conversations WHERE cnvs_dept IS NULL OR cnvs_dept = 0"

FETCH_GROUPS_QUERY = """
    SELECT DISTINCT a.agnt_name
    FROM agents a
    JOIN conversations c ON c.cnvs_agnt = a.agnt_id
    WHERE datetime(c.cnvs_created) BETWEEN ? AND ?
"""

SURVEY_DATA_METADATA_QUERY_ALL = """
    SELECT
        a.agnt_name,
        c.cnts_name,
        c.cnts_phone,
        cv.cnvs_id,
        cv.cnvs_created,
        cv.cnvs_updated,
        cv.cnvs_status,
        cv.cnvs_lang,
        cv.cnvs_software,
        cv.cnvs_tax_id,
        cv.cnvs_dept,
        cv.cnvs_rating_agent,
        cv.cnvs_rating_nps,
        cv.cnvs_contact_reason,
        cv.cnvs_occurrence,
        m.msgs_id,
        m.msgs_created,
        m.msgs_direction,
        m.msgs_agnt,
        qt.queue_time
    FROM messages m
    JOIN agents a ON m.msgs_agnt = a.agnt_id
    JOIN conversations cv ON m.msgs_cnvs = cv.cnvs_id
    JOIN contacts c ON cv.cnvs_cnts = c.cnts_id
    LEFT JOIN (
        SELECT m2.msgs_cnvs, MAX(m2.msgs_created) as queue_time
        FROM messages m2
        JOIN (
            SELECT msgs_cnvs, MIN(msgs_created) as first_agent_msg
            FROM messages
            WHERE msgs_agnt IS NOT NULL AND msgs_direction = 'sent'
            GROUP BY msgs_cnvs
        ) fa ON fa.msgs_cnvs = m2.msgs_cnvs
        WHERE m2.msgs_direction = 'received' AND m2.msgs_created <= fa.first_agent_msg
        GROUP BY m2.msgs_cnvs
    ) qt ON qt.msgs_cnvs = cv.cnvs_id
    ORDER BY cv.cnvs_id, m.msgs_created ASC
"""

OS_DATA_QUERY_ALL = """
SELECT
    c.cnvs_id,
    c.cnvs_bird,
    c.cnvs_agnt,
    c.cnvs_msgcount,
    c.cnvs_created,
    c.cnvs_updated,
    c.cnvs_dept,
    c.cnvs_contact_reason,
    c.cnvs_occurrence,
    c.cnvs_software,
    c.cnvs_rating_agent,
    c.cnvs_rating_nps,
    c.cnvs_reopened_count,
    c.cnvs_description,
    ct.cnts_id,
    ct.cnts_name,
    ct.cnts_phone,
    ct.cnts_custom1,
    ct.cnts_custom2,
    ct.cnts_custom3,
    ct.cnts_custom4,
    a.agnt_name,
    ROUND((julianday(c.cnvs_updated) - julianday(c.cnvs_created)) * 1440) as calc_duration_min
FROM conversations c
LEFT JOIN contacts ct ON ct.cnts_id = c.cnvs_cnts
LEFT JOIN agents a ON a.agnt_id = c.cnvs_agnt
ORDER BY c.cnvs_created
"""

FETCH_GROUPS_QUERY_ALL = """
    SELECT DISTINCT a.agnt_name
    FROM agents a
    JOIN conversations c ON c.cnvs_agnt = a.agnt_id
"""
