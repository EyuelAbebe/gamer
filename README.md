# gamer
=====

A repository for Code Fellows final project. Building an online game site.


## Resources

+ [Game Networking](http://gafferongames.com/networking-for-game-programmers/)
+ [Making a Chessboard with JS](http://chessboardjs.com/)
+ [Python Chat server/client](http://code.activestate.com/recipes/531824-chat-server-client-using-selectselect/)
+ [Web Chat & Socket.io ](http://blog.pythonisito.com/2012/07/realtime-web-chat-with-socketio-and.html)
+ [Sunfish Chess Engine in ~111 lines of Python](https://github.com/thomasahle/sunfish)
+ [Chess Symbols in Unicode](https://en.wikipedia.org/wiki/Chess_symbols_in_Unicode)


## Features

+ Deployment
 + AWS
    + Use RDS
    + One EC2
    + Fabric/boto
+ Testing
 + Everyone writes basic unit tests for their work
 + Functional testing
    + Selenium
+ Documentation
    + README
        + Installation
        + Usage
    + Docstrings
+ Database
 + Models
     + Player
        + Rating
        + Wins
        + Losses
        + Matches (game history)
        + Profile image
     + Game
        + White player
        + Black player
        + Move list
        + Outcome
        + Chat history
+ Registration
    + Django registration package
    + Allow anonymous users to play and chat
        + Generate unique anon name for each anon user
+ Game engine
    + start with sunfish?
    + write our own
        + Pieces as objects
        + Board contains pieces
        + Engine separate from board?
+ Game front end -- Duy
    + Static grid
    + Print pieces in new locations based on AJAX request
    + 3D board with perspective rotation?
    + End of match screen with winner, move list, and rating changes
+ Chat server
    + One lobby
    + One room per game
    + Unlimited number of participants
+ Site front end
    + Landing
    + Match in progress
    + Signup
    + User stats and profile
