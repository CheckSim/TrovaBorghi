from flask import Flask, render_template, request
import folium
import pandas as pd

app = Flask(__name__)

# Crea un DataFrame con nomi di città (puoi sostituirlo con il tuo dataset più grande)
df = pd.read_csv('./input/italian_municipalities.csv')
df.dropna(inplace = True)
df.sort_values('Città', inplace=True)
df.drop_duplicates(inplace=True)
df['Città_H'] = df['Città']
df['Città'] = df['Città'].str.lower()

access_counter = 0

@app.route('/')
def index():
    global access_counter
    access_counter += 1  # Incrementa il contatore ogni volta che viene visitata la pagina
    return render_template('index.html', access_counter=access_counter)

# Gestisce la ricerca e mostra i risultati
@app.route('/search', methods=['POST'])
def search():
    start_letters = request.form.get('start_letters').lower()
    end_letters = request.form.get('end_letters').lower()

    # Filtra le città per lettere iniziali e finali
    filtered_df = df[df['Città'].str.startswith(start_letters) & df['Città'].str.endswith(end_letters)]

    # Genera la mappa con Folium
    m = folium.Map(location=[41.9028, 12.4964], zoom_start=5)  # Centro Italia
    for _, row in filtered_df.iterrows():
        folium.Marker([row['Latitudine'], row['Longitudine']], popup=row['Città']).add_to(m)

    # Salva la mappa in un file HTML nella cartella static
    m.save('static/map.html')

    return render_template('results.html', cities=filtered_df['Città_H'].to_list(), map_html="map.html", ncities = len(filtered_df), access_counter=access_counter)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    #app.run(debug=True)
