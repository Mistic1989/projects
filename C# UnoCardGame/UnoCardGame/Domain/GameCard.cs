
namespace Domain;

public class GameCard
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public ECardColor CardColor { get; set; }
    public ECardValue CardValue { get; set; }
    public int Score { get; set; }
    
    public string DisplayCard { get; set; } = default!;
}