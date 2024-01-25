
namespace Domain;

public class Rule
{
    public EHouseRules? HouseRuleName { get; set; }
    
    public ECustomRules? CustomRuleName { get; set; }
    
    public ERuleType Type { get; set; }
    
    public string PromptMessage { get; set; } = default!;

    public string Info { get; set; } = default!;
    
    public string? DefaultValue { get; set; }
    
    public bool IsActive { get; set; }
    
    public object? SubjectToChange { get; set; }
}