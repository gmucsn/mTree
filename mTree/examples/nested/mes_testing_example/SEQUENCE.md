
```mermaid
  sequenceDiagram
    Environment->>Institution: Agent, endowment, auction items
    Institution->>Player 1: Item for auction
    Institution->>Player 2: Item for auction
    loop Wait for all bids
        Player 1->>Institution: Bid
        Player 2->>Institution: Bid        
        Institution->>Institution: Determine highest bidder
    end
    Institution->>Player 1: Final result 
    Institution->>Player 2: Final result
```