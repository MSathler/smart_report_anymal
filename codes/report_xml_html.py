import xml.etree.ElementTree as ET
import pandas as pd

class XML_TO_HTML:
    def __init__(self, path) -> None:
        self._path = path
        self._folder_path = path.split('report.xml')[0]
        self.main()

    def convert_time_format_UTC_to_BR(self, utc_str):
        utc = utc_str.split(':')
        return f'{int(utc[0])-3}:{utc[1]}:{utc[2]}'
    
    def main(self):
        print(self._path)
        tree = ET.parse(self._path)
        root = tree.getroot()
        files = []

        df = pd.DataFrame(columns=['Horário', 'Nome', 'Mensagem', 'Valor', 'Estado', 'Foto'])
        robot_name = root.find("robot").text

        date_raw = root.find("date").text.split('/')
        date = f'{date_raw[2]}/{date_raw[1]}/{date_raw[0]}'

        for entry in root.findall('entry'):
            level = entry.find('level').text
            if level == "INFO":
                time_of_day = self.convert_time_format_UTC_to_BR(entry.find('time_of_day').text)
                message = entry.find('message').text
                if entry.find('file').text is not None:
                    files.append(entry.find('file').text)
                try:
                    name = message.split("'")[1]
                except:
                    name = message
                value, status = '-', '-' 

                if 'took image' in message:
                    mission = (entry.find("author").text.split('/')[1]).split('/')[0]
                    message_t = f'Imagem tirada com sucesso de: {name}'
                elif 'analyzed temperature' in message:
                    status = entry.find('status').text
                    value = entry.find('value').text
                    message_t = f'Temperatura analisada com sucesso de: {name}'
                elif 'recorded video' in message:
                    mission = (entry.find("author").text.split('/')[1]).split('/')[0]
                    message_t = f'Filmagem realizada com sucesso de: {name}'
                elif 'recorded audio' in message:
                    mission = (entry.find("author").text.split('/')[1]).split('/')[0]
                    message_t = f'Audio gravado com sucesso de: {name}'
                else:
                    continue  

                temp_df = pd.DataFrame({
                    'Horário': [time_of_day],
                    'Nome': [name],
                    'Mensagem': [message_t],
                    'Valor': [value],
                    'Estado': [status],
                    'Foto': ['']
                })

                df = pd.concat([df, temp_df], ignore_index=True)

        for i, file in enumerate(files):
            if file.endswith('.mp4'):
                df.at[i, 'Foto'] = f'<video controls width="530" height="324"><source src="{file}" type="video/mp4">Your browser does not support the video tag.</video>'
            elif file.endswith('.wav'):
                df.at[i, 'Foto'] = f'<audio controls><source src="{file}" type="audio/wav">Your browser does not support the audio element.</audio>'
            else:
                df.at[i, 'Foto'] = f'<img src="{file}" width="530" height="324">'
        # Style the DataFrame
        styled_html = df.style.set_table_styles([
            {'selector': 'th', 'props': [('background-color', 'black'), 
                                        ('color', 'white'), 
                                        ('font-family', 'Arial'),
                                        ('border', '1px solid black')]},
            {'selector': 'td', 'props': [('background-color', 'white'), 
                                        ('color', 'black'), 
                                        ('font-family', 'Arial'),
                                        ('border', '1px solid black')]},
            {'selector': 'table, th, td', 'props': [('border-collapse', 'collapse'),
                                                    ('border', '1px solid black')]}
        ]).hide().to_html(escape=False)  # Using hide_index() to ensure the index is not shownn
        media_cells = df['Foto'].notnull()

        # Add a class attribute to the corresponding cells in the HTML string
        styled_html = styled_html.replace('<td>', '<td class="media-cell">', media_cells.sum())
        container = """
                    <title>Relatório da Missão</title>
                    <link rel="codes" href="templates/tecsath.ico" type="image/x-icon">
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            margin: 0;
                            padding: 0;
                            background-color: #f4f4f4;
                        }
                        .container {
                            max-width: 1300px;
                            margin: 20px auto;
                            padding: 20px;
                            background-color: #fff;
                            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                            border-radius: 5px;
                        }
                        .header {
                            text-align: center;
                            margin-bottom: 20px;
                        }
                        .header h1 {
                            color: #333;
                        }
                        .header p {
                            color: #666;
                            margin: 5px 0;
                        }
                        table {
                            width: 100%;
                            border-collapse: collapse;
                            margin-top: 20px;
                            
                        }
                        th, td {
                            border: 1px solid #ddd;
                            padding: 8px;
                            text-align: center;
                            overflow: hidden;
                            white-space: nowrap;
                            text-overflow: ellipsis;
                        }
                        th {
                            background-color: #f2f2f2;
                        }
                        tr:nth-child(even) {
                            background-color: #f9f9f9;
                        }
                        .image-container {
                            text-align: center;
                            margin-top: 20px;
                        }
                        .image-container,
                        .media-cell img {
                            max-width: 100%; /* Ensure images scale down on smaller screens */
                            height: auto;
                        }

                        /* Adjust media cell width */
                        .media-cell {
                            /* width: 40%; Remove or adjust the width for better responsiveness */
                            /* Other styles... */
                        }
                        @media only screen and (max-width: 600px) {
                            .media-cell {
                                width: 10%; /* Allow media cells to take full width on smaller screens */
                                /* Other specific styles for smaller screens... */
                            }
                        }
                    </style>
        """
        # Combine the page header and the HTML table
        html_string = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            {container}
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Relatório da Missão</h1>
                        <p><strong>Nome do Robô:</strong> {robot_name}</p>
                        <p><strong>Data:</strong> {date}</p>
                        <p><strong>Missão Executada:</strong> {mission}</p>
                    </div>
                    <div class="image-container">
                        <img src="./resources/image.png" alt="Robot Image">
                    </div>
                    <table>
                        <tbody>
                            {styled_html}
                        </tbody>
                    </table>
                </div>
            </body>
        </html>
        """

        # Save the HTML to a file
        with open(f'{self._folder_path}relatorio.html', 'w') as f:
            f.write(html_string)

if __name__ == '__main__':
    XML_TO_HTML('/Users/mauriciosathler/Desktop/itabira/ANYmal/2024-04-30/report.xml')