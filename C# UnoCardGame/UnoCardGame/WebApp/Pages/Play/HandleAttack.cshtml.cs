using System.Text;
using DAL;
using Domain;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using UnoEngine;

namespace WebApp.Pages.Play;

public class HandleAttack : PageModel
{
    private readonly AppDbContext _context;

    private IGameRepository _gameRepository;
    public GameEngine Engine { get; set; } = new();
    
    public GameEngineResults.HandlePlayerAttackResult? AttackResult { get; set; }
    
    public GameEngineResults.HandleAttackByPreviousPlayerResult? HandleAttackByPreviousPlayer { get; set; }
    
    public GameEngineResults.HandleDrawFourCardResult? HandleDrawFourCard { get; set; }
    public GameEngineResults.HandleChallengeResult? HandleChallenge { get; set; }
    public PlayerTurn? PreviousTurn { get; set; }
    public bool DirectionOfPlay { get; set; }
    
    [BindProperty(SupportsGet = true)]
    public Guid GameId { get; set; }

    [BindProperty(SupportsGet = true)]
    public Guid PlayerId { get; set; }
    public HandleAttack(AppDbContext context)
    {
        _context = context;
        _gameRepository = new GameRepositoryEF(_context);
    }
    
    public async Task OnGet()
    {
        Engine.State = _gameRepository.LoadGame(GameId);
        Engine.State.PlayerFinishedTurn = false;
        PreviousTurn = Engine.State.PreviousTurn;

        if (Engine.State.Message != null)
        {
            Engine.State.Message = null;
        }

        if (Engine.IsPlayerAttacked(PreviousTurn!))
        {
            AttackResult = Engine.HandlePlayerAttack(PreviousTurn!,
                Engine.State.CurrentPlayer!, PreviousTurn!.DeclaredColor);
            
            HandleAttackByPreviousPlayer = Engine.HandleAttackByPreviousPlayer(PreviousTurn.Card!,
                AttackResult.Player!, PreviousTurn.DeclaredColor);
            
            if (HandleAttackByPreviousPlayer.ShouldHandleDrawTwoCard)
            {
                Engine.HandleDrawTwoCard(AttackResult.Player!, HandleAttackByPreviousPlayer.PreviousTurn!,
                    HandleAttackByPreviousPlayer.StackCount);
                // WriteLine($"Player {attackResult.Player!.NickName}" +
                //           $" drew {handleAttackResult.StackCount * 2} cards!");
            }
            if (HandleAttackByPreviousPlayer.ShouldHandleDrawFourCard)
            {
                // WriteLine("Previous player played Draw Four card!");
                if (Engine.State.CurrentPlayer!.PlayerType == EPlayerType.Human)
                {
                    // WriteLine("Press 'c' to challenge previous player or 'Enter' to continue");
                }
                
                Engine.State.HandleDrawFourCard = true;
                // HandleDrawFourCard = Engine.HandleDrawFourCard(AttackResult.Player!,
                //     HandleAttackByPreviousPlayer.PreviousTurn!, HandleAttackByPreviousPlayer.StackCount, "");
                
                // if (HandleDrawFourCard.ShouldHandleChallenge)
                // {
                //     HandleChallenge = Engine.HandleChallenge(AttackResult.Player!,
                //         HandleAttackByPreviousPlayer.PreviousTurn!, HandleDrawFourCard.PreviousPlayer);
                //     if (HandleChallenge.DidCheat)
                //     {
                //         // WriteLine($"LAST PLAY CARD ON THE TABLE WAS:" +
                //         //                   $" {handleChallengeResult.PenultimateCard!.CardValue}" +
                //         //                   $" {handleChallengeResult.PenultimateCard!.CardColor}");
                //         // WriteLine();
                //         // WriteLine($"Previous player {handleDrawFourResult.PreviousPlayer!.NickName}" +
                //         //                   $" had these cards:");
                //         // handleDrawFourResult.PreviousPlayer!.Hand!.ForEach(x => 
                //         // WriteLine($"{x.CardValue}, {x.CardColor}"));
                //         // WriteLine($"{handleDrawFourResult.PreviousPlayer?.NickName}" +
                //         //                   $" cheated and draws 4 cards!");
                //     }
                //     else
                //     {
                //         // WriteLine($"{handleDrawFourResult.PreviousPlayer!.NickName} did not cheat!");
                //         // WriteLine($"Player {attackResult.Player!.NickName} who challenged" +
                //         //                   $" {handleDrawFourResult.PreviousPlayer!.NickName} will draw six cards!");
                //     }
                // }
                
                
                // if (HandleDrawFourCard.ShouldDrawCards && !HandleDrawFourCard.ShouldHandleChallenge)
                // {
                //     Engine.TakeDrawFourCards(AttackResult.Player!, HandleDrawFourCard.StackCount);
                //     // WriteLine($"Player {attackResult.Player!.NickName}" +
                //     //                   $" will draw {handleDrawFourResult.StackCount * 4} cards!");
                // }
            }
            
            // PreviousTurn = HandleAttackByPreviousPlayer.PreviousTurn;
            // Engine.State.PreviousPlayer = Engine.State.CurrentPlayer;
            
            if (Engine.State.SwitchToNextPlayer)
            {
                Engine.ChangePlayerIndex();
            }
        }

        Engine.State.PreviousTurn = PreviousTurn;
        DirectionOfPlay = Engine.HandlePlayDirection(PreviousTurn);
        
        await _gameRepository.SaveAsync(Engine.State);
        
        // return RedirectToPage("/Play/Index", new { gameId = GameId, playerId = PlayerId });
        
    }
    
    public async Task<IActionResult> OnPostSwitchPlayer()
    {
        Engine.State = _gameRepository.LoadGame(GameId);
        
        // if (HandleDrawFourCard != null && HandleDrawFourCard.ShouldDrawCards && !HandleDrawFourCard.ShouldHandleChallenge)
        // {
        //     Engine.TakeDrawFourCards(AttackResult!.Player!, HandleDrawFourCard.StackCount);
        //     // WriteLine($"Player {attackResult.Player!.NickName}" +
        //     //                   $" will draw {handleDrawFourResult.StackCount * 4} cards!");
        // }
        
        Engine.State.PreviousPlayerId = Engine.State.CurrentPlayer!.Id;
        await _gameRepository.SaveAsync(Engine.State);
        
        return RedirectToPage("/Play/Index", new { gameId = GameId, playerId = PlayerId});
    }
    
    // public async Task<IActionResult> OnPostHandleChallengeDrawFour(string input)
    // {
    //     StringBuilder message = new StringBuilder();
    //     Engine.State = _gameRepository.LoadGame(GameId);
    //     PreviousTurn = Engine.State.PreviousTurn;
    //     
    //     AttackResult = Engine.HandlePlayerAttack(PreviousTurn!,
    //         Engine.State.CurrentPlayer!, PreviousTurn!.DeclaredColor);
    //         
    //     HandleAttackByPreviousPlayer = Engine.HandleAttackByPreviousPlayer(PreviousTurn.Card!,
    //         AttackResult.Player!, PreviousTurn.DeclaredColor);
    //     
    //     HandleDrawFourCard = Engine.HandleDrawFourCard(AttackResult!.Player!,
    //         HandleAttackByPreviousPlayer!.PreviousTurn!, HandleAttackByPreviousPlayer.StackCount, input);
    //     
    //     HandleChallenge = Engine.HandleChallenge(AttackResult!.Player!,
    //     HandleAttackByPreviousPlayer.PreviousTurn!, HandleDrawFourCard!.PreviousPlayer);
    //     
    //     if (HandleDrawFourCard.ShouldDrawCards && !HandleDrawFourCard.ShouldHandleChallenge)
    //     {
    //         Engine.TakeDrawFourCards(AttackResult.Player!, HandleDrawFourCard.StackCount);
    //         // WriteLine($"Player {attackResult.Player!.NickName}" +
    //         //                   $" will draw {handleDrawFourResult.StackCount * 4} cards!");
    //     }
    //     if (HandleDrawFourCard.ShouldHandleChallenge)
    //     {
    //         HandleChallenge = Engine.HandleChallenge(AttackResult.Player!,
    //             HandleAttackByPreviousPlayer.PreviousTurn!, HandleDrawFourCard.PreviousPlayer);
    //         if (HandleChallenge.DidCheat)
    //         {
    //             // WriteLine($"LAST PLAY CARD ON THE TABLE WAS:" +
    //             //                   $" {handleChallengeResult.PenultimateCard!.CardValue}" +
    //             //                   $" {handleChallengeResult.PenultimateCard!.CardColor}");
    //             // WriteLine();
    //             // WriteLine($"Previous player {handleDrawFourResult.PreviousPlayer!.NickName}" +
    //             //                   $" had these cards:");
    //             // handleDrawFourResult.PreviousPlayer!.Hand!.ForEach(x => 
    //             // WriteLine($"{x.CardValue}, {x.CardColor}"));
    //             // WriteLine($"{handleDrawFourResult.PreviousPlayer?.NickName}" +
    //             //                   $" cheated and draws 4 cards!");
    //         }
    //         else
    //         {
    //             // WriteLine($"{handleDrawFourResult.PreviousPlayer!.NickName} did not cheat!");
    //             // WriteLine($"Player {attackResult.Player!.NickName} who challenged" +
    //             //                   $" {handleDrawFourResult.PreviousPlayer!.NickName} will draw six cards!");
    //         }
    //     }
    //     
    //     if (HandleDrawFourCard.ShouldDrawCards)
    //     {
    //         message.AppendLine($"Player {AttackResult.Player!.NickName} will draw {HandleDrawFourCard.StackCount * 4} cards!");
    //         // WriteLine($"Player {attackResult.Player!.NickName}" +
    //         //                   $" will draw {handleDrawFourResult.StackCount * 4} cards!");
    //     }
    //
    //     if (HandleDrawFourCard != null && HandleChallenge != null && HandleChallenge.DidCheat)
    //     {
    //         // WriteLine($"LAST PLAY CARD ON THE TABLE WAS:" +
    //         //                   $" {handleChallengeResult.PenultimateCard!.CardValue}" +
    //         //                   $" {handleChallengeResult.PenultimateCard!.CardColor}");
    //         // WriteLine();
    //         // WriteLine($"Previous player {handleDrawFourResult.PreviousPlayer!.NickName}" +
    //         //                   $" had these cards:");
    //         // handleDrawFourResult.PreviousPlayer!.Hand!.ForEach(x =>
    //         // WriteLine($"{x.CardValue}, {x.CardColor}"));
    //         // WriteLine($"{handleDrawFourResult.PreviousPlayer?.NickName}" +
    //         //                   $" cheated and draws 4 cards!");
    //         // <h1>@Model.HandleDrawFourCard.PreviousPlayer?.NickName was challenged</h1>
    //         // <h1>@Model.HandleDrawFourCard.PreviousPlayer?.NickName cheated and draws 4 cards!</h1>
    //         message.AppendLine($"{HandleDrawFourCard.PreviousPlayer?.NickName} was challenged");
    //         message.AppendLine($"{HandleDrawFourCard.PreviousPlayer?.NickName} cheated and draws 4 cards!");
    //     }
    //     
    //     if (HandleDrawFourCard != null && HandleChallenge != null && !HandleChallenge.DidCheat)
    //     {
    //         // <h1>@Model.HandleDrawFourCard.PreviousPlayer?.NickName did not cheat!</h1>
    //         // <h1>Player @Model.AttackResult.Player!.NickName who challenged @Model.HandleDrawFourCard.PreviousPlayer!.NickName will draw six cards!</h1>
    //         message.AppendLine($"{HandleDrawFourCard.PreviousPlayer?.NickName} did not cheat!");
    //         message.AppendLine($"{AttackResult.Player!.NickName} who challenged {HandleDrawFourCard.PreviousPlayer!.NickName} will draw six cards!");
    //     }
    //     
    //         // if (HandleChallenge.DidCheat)
    //         // {
    //         //     // WriteLine($"Previous player {HandleDrawFourCard.PreviousPlayer!.NickName}" +
    //         //     //                   $" had these cards:");
    //         //     // HandleDrawFourCard.PreviousPlayer!.Hand!.ForEach(x => 
    //         //     // WriteLine($"{x.CardValue}, {x.CardColor}"));
    //         //     // WriteLine($"{HandleDrawFourCard.PreviousPlayer?.NickName}" +
    //         //     //                   $" cheated and draws 4 cards!");
    //         // }
    //         // else
    //         // {
    //         //     // WriteLine($"{handleDrawFourResult.PreviousPlayer!.NickName} did not cheat!");
    //         //     // WriteLine($"Player {attackResult.Player!.NickName} who challenged" +
    //         //     //                   $" {handleDrawFourResult.PreviousPlayer!.NickName} will draw six cards!");
    //         // }
    //
    //     Engine.State.Message = message.ToString();
    //     Engine.State.HandleDrawFourCard = true;
    //     
    //     await _gameRepository.SaveAsync(Engine.State);
    //     
    //     return RedirectToPage("/Play/Index", new { gameId = GameId, playerId = PlayerId });
    // }
    
    public async Task SetMessage(string? message)
    {
        Engine.State.Message = message;
        await _gameRepository.SaveAsync(Engine.State);
    }
}