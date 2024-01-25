
using Domain;

namespace MenuSystem;

public class MenuItem
{
    public string ItemName { get; set; } = default!;
    public string Shortcut { get; set; } = default!;
    public Func<string>? UpdatePlayersCount { get; set; }
    public Func<string>? SelectedRules { get; set; }
    public Action<string?>? ToggleCustomRule { get; set; }
    public Action? ToggleHouseRule { get; set; }
    public Func<string?>? UpdateRules { get; set; }
    public Func<List<Player>>? UpdateNamesTypes { get; set; }
    public Func<string?>? MethodToRun { get; set; }
}