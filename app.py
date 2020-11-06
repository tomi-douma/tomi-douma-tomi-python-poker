from flask import Flask, render_template, request
from Casino.VideoPoker import VideoPoker

app = Flask(__name__)

vp = VideoPoker()

@app.route('/', methods=['POST','GET'])
def index():
    return render_template('index.html', bankroll=vp.get_bankroll(), resultat=vp.get_resultat())

@app.route('/start_part', methods=['POST','GET'])
def start_part():
    vp.init_deck()

    game_again = False

    if request.method == 'POST':
        game_again = True
    else:
        vp.set_bankroll(0)

    return render_template('start_part.html', decks=vp.decks(), game_again=game_again, bankroll=vp.get_bankroll())

@app.route('/bet', methods=['POST','GET'])
def bet():
    if request.method == 'POST':

        if len(request.form) == 2:
            bankroll = int(request.form['bankroll'])
            vp.set_bankroll((bankroll))

        mise = int(request.form['mise'])

        vp.set_mise(mise)

        hands, decks = vp.premier_tirage()


        return render_template('bet.html', hands=hands, decks=decks, bankroll=vp.get_bankroll())


@app.route('/game', methods=['POST','GET'])
def game():
    if request.method == 'POST':

        draws = list(request.form) #todo draw

        final_draws = vp.deuxieme_tirage(draws)

        resultat, bankroll, msg = vp.video_poker(final_draws)

        return render_template('game.html', final_draws=final_draws, decks=vp.decks(), resultat=vp.get_resultat(), bankroll=vp.get_bankroll(), msg=msg)


if __name__ == "__main__":
    app.run(debug=True)
