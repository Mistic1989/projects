
namespace Domain;

public class GameState
{
    public Guid Id { get; set; } = Guid.NewGuid();
    
    public List<Player> Players { get; set; } = new List<Player>();
    
    public List<GameCard> DrawPile { get; set; } = new List<GameCard>();
    
    public List<GameCard> DiscardPile { get; set; } = new List<GameCard>();

    public Stack<PlayerTurn> PlayerTurns { get; set; } = new Stack<PlayerTurn>();
    
    public PlayerTurn? PreviousTurn { get; set; }
    
    public string? Message { get; set; }
    
    public bool HandleDrawFourCard { get; set; }
    
    public bool PlayerFinishedTurn { get; set; }
    
    public List<Stack<PlayerTurn>> GameRounds { get; set; } = new List<Stack<PlayerTurn>>();
    
    public GameCard? CurrentPlayCardOnTheTable { get; set; }
    
    public GameCard? SelectedCardByPlayer { get; set; }

    public Player? CurrentPlayer { get; set; }
    
    public Guid? PreviousPlayerId { get; set; }
    
    public bool ShoutedUno { get; set; }
    
    public Player? Winner { get; set; }
    
    public Rules Rules { get; set; } = new Rules();

    public int PlayerIndex { get; set; }

    public DirectionOfPlay DirectionOfPlay { get; set; } = DirectionOfPlay.Clockwise;

    public Player? Dealer { get; set; }
    
    public bool ExitGame { get; set; }
    
    public bool RoundOver { get; set; }
    public bool GameOver { get; set; }
    
    public bool SwitchToNextPlayer { get; set; }
}