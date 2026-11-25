CREATE OR ALTER PROCEDURE dbo.SampleReport
    @Site NVARCHAR(50),
    @SortColumn NVARCHAR(128)
AS
BEGIN
    -- Called by the reporting API with values from the query string.
    DECLARE @sql NVARCHAR(MAX) =
        N'SELECT sample_id, site, concentration_mg_l FROM dbo.samples WHERE site = ''' + @Site
        + N''' ORDER BY ' + @SortColumn;
    EXEC(@sql);
END
