using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Design;

namespace DAL;

public class AppDbContextFactory : IDesignTimeDbContextFactory<AppDbContext>
{
    
    public AppDbContext CreateDbContext(string[] args)
    {
        // var appData = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
        //
        // var connectionString = "DataSource=<%temppath%>uno.db;Cache=Shared";
        // connectionString = connectionString.Replace("<%temppath%>", appData);
        
        var optionsBuilder = new DbContextOptionsBuilder<AppDbContext>();
        optionsBuilder.UseSqlite("");

        return new AppDbContext(optionsBuilder.Options);
    }
}