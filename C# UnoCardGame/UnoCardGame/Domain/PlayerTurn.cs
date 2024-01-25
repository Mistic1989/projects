namespace Domain;

public class PlayerTurn
{
    public GameCard? Card { get; set; }
    public TurnResult Result { get; set; }
    
    public ECardColor? DeclaredColor { get; set; }
    
    public bool DidCheat { get; set; }
    
    public bool DidShoutUno { get; set; }
    
    public bool ChallengedSuccessfully { get; set; }

    public bool StackCards { get; set; }

    public int StackCount { get; set; } = 1;
    
    public Player? Player { get; set; }
}
    
