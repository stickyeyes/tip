--USE [sord_dev_will]
--GO
--EXEC [dbo].[rpt_competency_ge2013_proc]
--GO

DECLARE @competency_id INT
SET @competency_id = 1

DECLARE @year INT

;WITH years ( year ) AS
(
SELECT DISTINCT student_class_of
  FROM rpt_competency_ge2013_metric metric
    WHERE competency_id = @competency_id
    AND ( @year IS NULL OR @year = 0 OR student_class_of IN ( @year ) )
UNION
SELECT 1775
)
SELECT * FROM years
--SELECT title, student_class_of, value, [order]
--FROM years
--LEFT OUTER JOIN rpt_competency_ge2013_metric metric ON metric.student_class_of = years.year
--INNER JOIN rpt_competency_ge2013_func func ON func.id = metric.func_id
--WHERE competency_id = @competency_id
--ORDER BY [order] ASC