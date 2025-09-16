from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# --- APP ve DB ---
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- MODEL ---
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))

# --- TABLOLARI OLUŞTUR ---
with app.app_context():
    db.create_all()

# --- ROUTE: ANA SAYFA ---
@app.route('/')
@app.route('/index')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

# --- ROUTE: YENİ ÖĞE EKLE ---
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        db.session.add(Item(
            name=request.form['name'],
            description=request.form['description']
        ))
        db.session.commit()
        return redirect('/')
    return render_template('create.html')

# --- ROUTE: ÖĞEYİ GÜNCELLE ---
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    item = Item.query.get_or_404(id)
    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        db.session.commit()
        return redirect('/')
    return render_template('update.html', item=item)

# --- ROUTE: ÖĞEYİ SİL ---

@app.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect('/')
    # --- ROUTE: ÖĞEYİ SİL 
  # ---@app.route('/delete/<int:id>')
  # ---def delete(id):
      # ---item = Item.query.get_or_404(id)
      # ---db.session.delete(item)
      # ---db.session.commit()
      # ---return redirect('/')

# --- SERVERI BAŞLAT ---
if __name__ == '__main__':
    app.run(debug=True)
