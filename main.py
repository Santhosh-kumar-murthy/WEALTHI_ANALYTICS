from flask import Flask, jsonify, request, render_template, redirect

from controller.positions_controller import PositionsController

app = Flask(__name__)

positions_controller = PositionsController()


@app.route('/')
def index():
    return redirect('idx_positions?status=active')


@app.route('/idx_positions')
def idx_positions():
    status = request.args.get('status')
    if status not in ['active', 'closed']:
        return jsonify({'error': 'Invalid status. Use "active" or "closed".'}), 400
    positions = positions_controller.get_index_positions(status)
    return render_template('idx_positions.html', positions=positions, title="INDEX POSITIONS " + status)


@app.route('/opt_positions')
def opt_positions():
    status = request.args.get('status')
    position_type = request.args.get('position_type')
    if position_type == '1':
        position_type_title = "OPTIONS BUYING"
    elif position_type == '2':
        position_type_title = "OPTIONS SELLING"
    else:
        position_type_title = "OPTIONS FUCKING"

    if status not in ['active', 'closed']:
        return jsonify({'error': 'Invalid status. Use "active" or "closed".'}), 400
    if position_type not in ['1', '2']:
        return jsonify({'error': 'Invalid position_type. Use "1" for Buy or "2" for Sell.'}), 400
    positions = positions_controller.get_option_positions(position_type, status)
    return render_template('opt_positions.html', positions=positions, title="OPTIONS POSITIONS " + status,
                           position_type_title=position_type_title)


if __name__ == '__main__':
    app.run(debug=True)
