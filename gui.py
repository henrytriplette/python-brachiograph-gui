import PySimpleGUI as sg
import paramiko
import cairosvg

from linedraw import *

from pathlib import Path, PureWindowsPath
from datetime import datetime

def main():

    sg.change_look_and_feel('Reddit')

    # make these elements outside the layout because want to "update" them later
    image_elem = sg.Image(filename = 'temp/blank.png')

    menu = [
            [sg.Text('Convert Image to JSON')],
            [sg.Text('Content Image', size=(15, 1)), sg.Input(key='content_image'), sg.FileBrowse(file_types=(('Images', '*.jpg'),('PNG', '*.png')))],
            [sg.Text('Contours', auto_size_text=True)],
            [sg.Slider(range=(1, 100), orientation='h', size=(45, 15), default_value=2, resolution=0.5, key='draw_contours', tooltip='Start with a draw_contours of 2, and then values between 0.5 and 4.')],
            [sg.Text('Hatch', auto_size_text=True)],
            [sg.Slider(range=(1, 100), orientation='h', size=(45, 15), default_value=16, key='draw_hatch', tooltip='Start with a draw_hatch of 16, and then values between 8 and 16.')],
            [sg.Text('Repeat Contours', auto_size_text=True)],
            [sg.Slider(range=(0, 100), orientation='h', size=(45, 15), default_value=0, key='repeat_contours', tooltip='For example, repeat_contours=3 means that the contour data will be added to the JSON file three times in succession; the effect will be to draw them three times instead of just once, so the edges of the final image stand out.')],
            [sg.Button('Process Files', key='generate')],
            [sg.Text('_' * 80)],
            [sg.Text('Upload JSON to Raspberry Pi')],
            [sg.Text('FTP IP', size=(15, 1)), sg.InputText('192.168.1.157', key='ftp_ip')],
            [sg.Text('FTP User', size=(15, 1)), sg.InputText('pi', key='ftp_user')],
            [sg.Text('FTP Password', size=(15, 1)), sg.InputText('raspberry', key='ftp_password')],
            [sg.Text('FTP Path', size=(15, 1)), sg.InputText('/home/pi/Brachiograph/patterns/', key='ftp_path')],
            [sg.Text('JSON Pattern', size=(15, 1)), sg.Input(key='ftp_file'), sg.FileBrowse()],
            [sg.Button('Upload Files', key='upload')],
            [sg.Text('_' * 80)],
            [sg.Cancel(key='quit')],
             ]

    layout = [
                [sg.Column(menu), image_elem]
            ]

    window = sg.Window('Brachiograph Utility', layout)


    while (True):

        # This is the code that reads and updates your window
        event, values = window.Read(timeout=100)

        if event == 'Exit' or event is None:
            break

        if event == 'quit':
            break

        if event == 'generate':
            print('Begin JSON generation')

            # Convert
            image_to_json(
                values['content_image'],
                draw_contours=int(values['draw_contours']),
                draw_hatch=int(values['draw_hatch']),
                repeat_contours=int(values['repeat_contours']),
            )

            # Display
            inputSvg = 'images/' + Path(values['content_image']).stem + '.svg'
            outputPng = 'temp/converted.png'
            cairosvg.svg2png(url=inputSvg, write_to=outputPng, parent_width=512, parent_height=512)
            image_elem.Update(filename = outputPng)

        if event == 'upload':
            print('Begin FTP file Upload')

            # SFTP Upload
            try:
                transport = paramiko.Transport((values['ftp_ip'] ,22))
                transport.connect(username=values['ftp_user'], password=values['ftp_password'])
                sftp = paramiko.SFTPClient.from_transport(transport)

                print('Connection succesfully stablished ... ')
                localFilePath = values['ftp_file']

                # Define the remote path where the file will be uploaded
                remoteFilename = Path(values['ftp_file']).stem + '.json'
                remoteFilePath = values['ftp_path'] + remoteFilename

                sftp.put(localFilePath, remoteFilePath)
                sftp.close()

                single_datestring = datetime.strftime(datetime.now(), '%Y-%m-%d_%H.%M.%S')
                sg.Popup('Completed', 'Upload completed at ' + single_datestring)
            except:
                sg.Popup('ERROR', 'Please check the connection parameters')

    window.Close()   # Don't forget to close your window!

if __name__ == '__main__':
    main()
