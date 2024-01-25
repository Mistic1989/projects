
using UnoEngine;

namespace Domain;

public class Player
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public string NickName { get; set; } = default!;
    public EPlayerType PlayerType { get; set; }

    public List<GameCard>? Hand { get; set; }
    
    public int Position { get; set; }
    
    public int Score { get; set; }
    
    public Guid GameId { get; set; }
    
    // public Game? Game { get; set; }
    
}