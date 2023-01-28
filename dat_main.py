
from pathlib import Path
from tempfile import NamedTemporaryFile
import io
# import zipfile

import streamlit as st
import matplotlib.pyplot as plt
import japanize_matplotlib

from acdatconv import datconv as dv
from acdatconv import datlib as dlib

st.title('AC Dat File Converter')

# Fileの拡張子をチェックしてくる
uploaded_file = st.file_uploader("dat file upload", type='dat')


if uploaded_file is not None:
    file_name = uploaded_file.name
    save_name = file_name.split('.')[0]

    
    with NamedTemporaryFile(delete=False) as f:
        fp = Path(f.name)
        fp.write_bytes(uploaded_file.getvalue())
        
        acdata = dv.AcConv(f'{f.name}')
        acdata.convert()
        
    # ファイルを削除  
    fp.unlink()
    # st.write(acdata.estimate_value)
    
    fig =plt.figure() 
    ax = fig.add_subplot(111)
    ax.set_title(f'{acdata.metadata["sampleName"]}')
    ax.plot(acdata.df["uvEnergy"],acdata.df["npyield"],'ro-',label='Data')
    ax.plot(acdata.df["uvEnergy"],acdata.df["guideline"],'b-',label=f'Estimate line\n {acdata.metadata["thresholdEnergy"]:.2f} eV')
    ax.legend()
    ax.grid()
    ax.set_xlabel('energy [eV]')
    ax.set_ylabel(f'Intensity^{acdata.metadata["powerNumber"]:.2f}')
    
    # メモリに保存
    img = io.BytesIO()
    plt.savefig(img, format='png')
    
    st.pyplot(fig)
    
    csv = acdata.df[["uvEnergy","pyield","npyield",	"nayield","guideline"]].to_csv(index=False)
    json = acdata.json

    # ボタンを横に並べるため
    col1, col2, col3 = st.columns([1,1,1])
    
    with col1:
        st.download_button(label='Download csv data', 
                        data=csv, 
                        file_name=f'{save_name}.csv',
                        mime='text/csv',
                        )
    with col2:
        st.download_button(label="Download image",
                        data=img,
                        file_name=f'{save_name}.png',
                        mime="image/png"
                        )
    with col3:    
        st.download_button(label ="Download json",
                        data=json,
                        file_name=f'{save_name}.json',
                        mime="application/json",
                        )
    
    # TODO: Zipでダウンロードできるようにする
    


        
    

