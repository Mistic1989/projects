# icd0008-23f

Name: Alo Ansberg
Uni-id: alansb
Student code: 223450
e-mail: alansb@taltech.ee

## EF

~~~bash
dotnet tool update --global dotnet-ef

dotnet ef migrations add --project DAL --startup-project ConsoleApp InitialCreate
dotnet ef migrations add --project DAL --startup-project WebApp InitialCreate

dotnet ef database update --project DAL --startup-project WebApp
~~~

## WebApp

~~~bash
dotnet tool update --global dotnet-aspnet-codegenerator
cd WebApp
dotnet aspnet-codegenerator razorpage -m Domain.Database.Game -dc AppDbContext -udl -outDir Pages/Games --referenceScriptLibraries
dotnet aspnet-codegenerator razorpage -m Domain.Database.Player -dc AppDbContext -udl -outDir Pages/Players --referenceScriptLibraries
~~~