using System.Text;
using DAL;
using Domain;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using UnoEngine;

namespace WebApp.Pages.Play;

public class Index : PageModel
{
    private readonly AppDbContext _context;

    private IGameRepository _gameRepository;
    
    // private readonly IWebHostEnvironment _hostingEnvironment;
    
    public GameEngine Engine { get; set; } = new();
    
    public Index(AppDbContext context)
    {
        _context = context;
        
        // _hostingEnvironment = hostingEnvironment;
        
        _gameRepository = new GameRepositoryEF(_context);
        
        bool useFileSystem = false;
        
        if (useFileSystem)
        {
            // _gameRepository = new GameRepositoryFileSystem(Engine.State, _hostingEnvironment);
        }
        else
        {
            _gameRepository = new GameRepositoryEF(_context);
        }
    }

    [BindProperty(SupportsGet = true)]
    public Guid GameId { get; set; }

    [BindProperty(SupportsGet = true)]
    public Guid PlayerId { get; set; }
    
    [BindProperty(SupportsGet = true)]
    public Guid? PreviousPlayerId { get; set; }
    
    public PlayerTurn? PreviousTurn { get; set; }
    
    public GameEngineResults.HandleChallengeResult? HandleChallenge { get; set; }
    
    public GameEngineResults.HandlePlayerAttackResult? AttackResult { get; set; }
    public GameEngineResults.HandleAttackByPreviousPlayerResult? HandleAttackByPreviousPlayer { get; set; }

    public GameEngineResults.HandleDrawFourCardResult? HandleDrawFourCard { get; set; }

    public GameEngineResults.DrawCardResult? DrawCardResult { get; set; }
    
    public GameEngineResults.CheckIfLastPlayerShoutedUnoResult? PlayerShoutedUno { get; set; }
    
    public Player ChosenPlayer { get; set; } = default!;
    
    public GameCard? SelectedCardByPlayer { get; set; }
    
    public List<GameCard> PlayableCards { get; set; } = new();
    
    public GameEngineResults.HandlePlayCardResult? PlayCardResult { get; set; }
    
    public GameEngineResults.HandleDeclareColorResult? DeclareColorResult { get; set; }
    
    public void OnGet()
    {
        Engine.State = _gameRepository.LoadGame(GameId);
        if (Engine.State.PreviousTurn != null)
        {
            PreviousTurn = Engine.State.PreviousTurn;
        }
        else
        {
            PreviousTurn = Engine.State.PlayerTurns.Count > 1 ? Engine.State.PlayerTurns.Peek() : null; 
        }
        
        ChosenPlayer = Engine.State.Players.First(x => x.Id == PlayerId);
        PlayableCards = Engine.PlayableCards(Engine.State.CurrentPlayer!, PreviousTurn!.DeclaredColor);
    }
    
    public async Task OnPostPreviousPlayerShoutedUno()
    {
        Engine.State = _gameRepository.LoadGame(GameId);
        if (Engine.State.PreviousTurn != null)
        {
            PreviousTurn = Engine.State.PreviousTurn;
            PlayerShoutedUno = Engine.HandleIfLastPlayerShoutedUno(PreviousTurn!, "c");
        }
        else
        {
            PreviousTurn = Engine.State.PlayerTurns.Count > 1 ? Engine.State.PlayerTurns.Peek() : null; 
        }
        
        ChosenPlayer = Engine.State.Players.First(x => x.Id == PlayerId);
        PlayableCards = Engine.PlayableCards(Engine.State.CurrentPlayer!, PreviousTurn!.DeclaredColor);
        Engine.State.ShoutedUno = false;
        
        await _gameRepository.SaveAsync(Engine.State);
    }

    public async Task OnPostSelectCard(Guid selectedCard)
    {
        Engine.State = _gameRepository.LoadGame(GameId);
        if (Engine.State.PreviousTurn != null)
        {
            PreviousTurn = Engine.State.PreviousTurn;
        }
        else
        {
            PreviousTurn = Engine.State.PlayerTurns.Count > 1 ? Engine.State.PlayerTurns.Peek() : null; 
        }
        // PreviousTurn = Engine.State.PlayerTurns.Count > 1 ? Engine.State.PlayerTurns.Peek() : null;
        // PlayerId = Engine.State.CurrentPlayer!.Id;
        ChosenPlayer = Engine.State.Players.First(x => x.Id == PlayerId);

        var choice = (Engine.State.CurrentPlayer!.Hand!.FindIndex(x => x.Id == selectedCard) + 1).ToString();
            
        var playerChooseCardResult = Engine.State.CurrentPlayer!.PlayerType == EPlayerType.Human
            ? Engine.HumanChooseCard(Engine.State.CurrentPlayer, PreviousTurn!.DeclaredColor, choice)
            : Engine.AiChooseCard(Engine.State.CurrentPlayer, PreviousTurn!.DeclaredColor);
        
        SelectedCardByPlayer = playerChooseCardResult.SelectedCard;
        
        var playMatchingCardResult = Engine.PlayMatchingCard(SelectedCardByPlayer, PreviousTurn.DeclaredColor);
        if (playMatchingCardResult.PlayNoMatchingCard)
        {
            PreviousTurn = playMatchingCardResult.PlayerTurn;
        }

        PlayMatchingCardResult(playMatchingCardResult);
        Engine.State.PreviousTurn = PreviousTurn;
        Engine.State.SelectedCardByPlayer = SelectedCardByPlayer;
        
        await _gameRepository.SaveAsync(Engine.State);
    }
    
    public async Task OnPostDrawCard()
    {
        Engine.State = _gameRepository.LoadGame(GameId);
        if (Engine.State.PreviousTurn != null)
        {
            PreviousTurn = Engine.State.PreviousTurn;
        }
        else
        {
            PreviousTurn = Engine.State.PlayerTurns.Count > 1 ? Engine.State.PlayerTurns.Peek() : null; 
        }
        // PreviousTurn = Engine.State.PlayerTurns.Count > 1 ? Engine.State.PlayerTurns.Peek() : null;
        // PlayerId = Engine.State.CurrentPlayer!.Id;
        ChosenPlayer = Engine.State.Players.First(x => x.Id == PlayerId);
        
        DrawCardResult = Engine.DrawCard(Engine.State.CurrentPlayer!, PreviousTurn!.DeclaredColor);
        GameCard? selectedCard = Engine.CheckIfForceDrawPlay(DrawCardResult.PlayerTurn!);
        SelectedCardByPlayer = selectedCard;

        var playMatchingCardResult = Engine.PlayMatchingCard(SelectedCardByPlayer, PreviousTurn.DeclaredColor);
        if (playMatchingCardResult.PlayNoMatchingCard)
        {
            PreviousTurn = playMatchingCardResult.PlayerTurn;
        }
        
        PlayMatchingCardResult(playMatchingCardResult);
        
        Engine.State.SelectedCardByPlayer = SelectedCardByPlayer;
        Engine.State.PreviousTurn = PreviousTurn;
        await _gameRepository.SaveAsync(Engine.State);    
    }
    
    public async Task OnPostSelectColor(string selectedColor)
    {
        Engine.State = _gameRepository.LoadGame(GameId);
        PreviousTurn = Engine.State.PreviousTurn;
        // PlayerId = Engine.State.CurrentPlayer!.Id;
        ChosenPlayer = Engine.State.Players.First(x => x.Id == PlayerId);
        
        DeclareColorResult = Engine.DeclareColor(PreviousTurn!, selectedColor);
        PreviousTurn!.DeclaredColor = DeclareColorResult.PlayerTurn!.DeclaredColor;
        
        SelectedCardByPlayer = Engine.State.SelectedCardByPlayer;
        Engine.State.PreviousTurn = PreviousTurn;
        Engine.State.PlayerFinishedTurn = true;
        
        await _gameRepository.SaveAsync(Engine.State);
        
    }
    
    public async Task<IActionResult> OnPostSwitchToNextPlayer(string? shoutUno)
    {
        Engine.State = _gameRepository.LoadGame(GameId);
        PreviousTurn = Engine.State.PreviousTurn;
        
        if (PreviousTurn!.Result != TurnResult.Reversed)
        {
            Engine.State.PlayerIndex = Engine.NextPlayerIndex(Engine.State.PlayerIndex);
            Engine.State.CurrentPlayer = Engine.State.Players[Engine.State.PlayerIndex];
        }

        if (shoutUno == "s")
        {
            Engine.HandleUnoShout(PreviousTurn!, "s");
            Engine.State.PreviousTurn = PreviousTurn;
            Engine.State.ShoutedUno = true;
        }
        
        Engine.State.HandleDrawFourCard = false;
        
        await _gameRepository.SaveAsync(Engine.State);
        
        return RedirectToPage("./HandleAttack", new { gameId = GameId, playerId = PlayerId });
    }
    
    // public async Task<IActionResult> OnPostHandleChallengeDrawFour(string? challengeDrawFour)
    // {
    //     // StringBuilder message = new StringBuilder();
    //     Engine.State = _gameRepository.LoadGame(GameId);
    //     PreviousTurn = Engine.State.PreviousTurn;
    //     ChosenPlayer = Engine.State.Players.First(x => x.Id == PlayerId);
    //     
    //     AttackResult = Engine.HandlePlayerAttack(PreviousTurn!,
    //         Engine.State.CurrentPlayer!, PreviousTurn!.DeclaredColor);
    //         
    //     HandleAttackByPreviousPlayer = Engine.HandleAttackByPreviousPlayer(PreviousTurn.Card!,
    //         AttackResult.Player!, PreviousTurn.DeclaredColor);
    //
    //     var challenge = challengeDrawFour == null ? "" : "c";
    //
    //     HandleDrawFourCard = Engine.HandleDrawFourCard(AttackResult.Player!,
    //         HandleAttackByPreviousPlayer.PreviousTurn!, HandleAttackByPreviousPlayer.StackCount, challenge);
    //     
    //     if (HandleDrawFourCard.ShouldDrawCards && !HandleDrawFourCard.ShouldHandleChallenge)
    //     {
    //         Engine.TakeDrawFourCards(AttackResult!.Player!, HandleDrawFourCard.StackCount);
    //         // WriteLine($"Player {attackResult.Player!.NickName}" +
    //         //                   $" will draw {handleDrawFourResult.StackCount * 4} cards!");
    //     }
    //     else
    //     {
    //         HandleChallenge = Engine.HandleChallenge(AttackResult!.Player!,
    //             HandleAttackByPreviousPlayer.PreviousTurn!, HandleDrawFourCard!.PreviousPlayer);
    //     }
    //     // if (HandleChallenge.DidCheat)
    //     // {
    //     //     // WriteLine($"Previous player {HandleDrawFourCard.PreviousPlayer!.NickName}" +
    //     //     //                   $" had these cards:");
    //     //     // HandleDrawFourCard.PreviousPlayer!.Hand!.ForEach(x => 
    //     //     // WriteLine($"{x.CardValue}, {x.CardColor}"));
    //     //     // WriteLine($"{HandleDrawFourCard.PreviousPlayer?.NickName}" +
    //     //     //                   $" cheated and draws 4 cards!");
    //     // }
    //     // else
    //     // {
    //     //     // WriteLine($"{handleDrawFourResult.PreviousPlayer!.NickName} did not cheat!");
    //     //     // WriteLine($"Player {attackResult.Player!.NickName} who challenged" +
    //     //     //                   $" {handleDrawFourResult.PreviousPlayer!.NickName} will draw six cards!");
    //     // }
    //     
    //     
    //     await _gameRepository.SaveAsync(Engine.State);
    //     
    //     return RedirectToPage("/Play/Index", new { gameId = GameId, playerId = PlayerId });
    // }
    
    // public async Task<IActionResult> OnPostShoutUno()
    // {
    //     Engine.State = _gameRepository.LoadGame(GameId);
    //     PreviousTurn = Engine.State.PreviousTurn;
    //     // ChosenPlayer = Engine.State.Players.First(x => x.Id == PlayerId);
    //     
    //     Engine.HandleUnoShout(PreviousTurn!, "s");
    //     
    //     // SelectedCardByPlayer = Engine.State.SelectedCardByPlayer;
    //     Engine.State.PreviousTurn = PreviousTurn;
    //     
    //     await _gameRepository.SaveAsync(Engine.State);
    //     
    //     return RedirectToPage("./HandleAttack", new { gameId = GameId, playerId = PlayerId });
    // }
    
    public async Task OnPostHandleChallengeDrawFour(string input)
    {
        StringBuilder message = new StringBuilder();
        Engine.State = _gameRepository.LoadGame(GameId);
        PreviousTurn = Engine.State.PreviousTurn;
        ChosenPlayer = Engine.State.Players.First(x => x.Id == PlayerId);
        PreviousPlayerId = Engine.State.PreviousPlayerId;
        Engine.State.CurrentPlayer = Engine.State.Players[Engine.State.PlayerIndex];
        
        AttackResult = Engine.HandlePlayerAttack(PreviousTurn!,
            Engine.State.CurrentPlayer!, PreviousTurn!.DeclaredColor);
            
        HandleAttackByPreviousPlayer = Engine.HandleAttackByPreviousPlayer(PreviousTurn.Card!,
            AttackResult.Player!, PreviousTurn.DeclaredColor);

        if (input != "c")
        {
            input = "";
        }
        
        HandleDrawFourCard = Engine.HandleDrawFourCard(AttackResult!.Player!,
            HandleAttackByPreviousPlayer!.PreviousTurn!, HandleAttackByPreviousPlayer.StackCount, input);
        
        PreviousTurn = HandleAttackByPreviousPlayer.PreviousTurn;
        
        if (HandleDrawFourCard.ShouldDrawCards)
        {
            Engine.TakeDrawFourCards(AttackResult.Player!, HandleDrawFourCard.StackCount);
            // Engine.State.CurrentPlayer = AttackResult.Player!;
            PreviousTurn = AttackResult.PreviousTurn;
            message.AppendLine($"Player {Engine.State.CurrentPlayer!.NickName} will draw {HandleDrawFourCard.StackCount * 4} cards!");
            // WriteLine($"Player {attackResult.Player!.NickName}" +
            //                   $" will draw {handleDrawFourResult.StackCount * 4} cards!");
        }

        if (HandleDrawFourCard.ShouldHandleChallenge)
        {
            HandleChallenge = Engine.HandleChallenge(AttackResult!.Player!,
                HandleAttackByPreviousPlayer.PreviousTurn!, HandleDrawFourCard!.PreviousPlayer);
            
            PreviousTurn = HandleChallenge.PlayerTurn;

            if (HandleChallenge.DidCheat)
            {
                message.AppendLine(
                    $"{Engine.State.Players.FirstOrDefault(x => x.Id == PreviousPlayerId)!.NickName} was challenged.");
                message.AppendLine(
                    $"{Engine.State.Players.FirstOrDefault(x => x.Id == PreviousPlayerId)!.NickName} cheated and draws 4 cards!");
            }

            else
            {
                // <h1>@Model.HandleDrawFourCard.PreviousPlayer?.NickName did not cheat!</h1>
                // <h1>Player @Model.AttackResult.Player!.NickName who challenged @Model.HandleDrawFourCard.PreviousPlayer!.NickName will draw six cards!</h1>
                message.AppendLine(
                    $"{Engine.State.Players.FirstOrDefault(x => x.Id == PreviousPlayerId)!.NickName} did not cheat!");
                message.AppendLine(
                    $"{Engine.State.CurrentPlayer!.NickName} who challenged {Engine.State.Players.FirstOrDefault(x => x.Id == PreviousPlayerId)!.NickName} will draw six cards!");
            }
        }

        Engine.State.Message = message.ToString();
        Engine.State.HandleDrawFourCard = false;

        if (HandleChallenge != null && !HandleChallenge.DidCheat)
        {
            Engine.ChangePlayerIndex();
        }
        
        PlayableCards = Engine.PlayableCards(Engine.State.CurrentPlayer!, PreviousTurn!.DeclaredColor);
        Engine.State.PreviousTurn = PreviousTurn;
        
        await _gameRepository.SaveAsync(Engine.State);
        
        // return RedirectToPage("/Play/Index", new { gameId = GameId, playerId = PlayerId });
    }
    
    private void PlayMatchingCardResult(GameEngineResults.PlayMatchingCardResult playMatchingCardResult)
    {
        if (playMatchingCardResult.PlayCard)
        {
            PlayCardResult = Engine.PlayCard(Engine.State.CurrentPlayer!, SelectedCardByPlayer!);
            PreviousTurn = PlayCardResult.PlayerTurn;
            
            if (PlayCardResult.ShouldDeclareColor)
            {
                if (Engine.State.CurrentPlayer!.PlayerType == EPlayerType.AI)
                {
                    PreviousTurn!.DeclaredColor = Engine.AiColorDeclaration(Engine.State.CurrentPlayer); 
                }
            }
            else
            {
                Engine.State.PlayerFinishedTurn = true;
            }
        }
        
        _gameRepository.SaveAsync(Engine.State);
    }
    
    public async Task SetMessage(string? message)
    {
        Engine.State.Message = message;
        await _gameRepository.SaveAsync(Engine.State);
    }
}

