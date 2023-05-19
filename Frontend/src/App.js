import React, { useState } from 'react';
import './App.css';
import '../node_modules/bootstrap/dist/css/bootstrap.css';
import Slide from './slide.png';
function App() {

  const [ title, setTitle ] = useState("");
  const [ cover, setCever ] = useState();
  const [ file, setfile] = useState("Convert");
  const [ download, setdownload] = useState("");
  const newBook = () => {
    const uploadData = new FormData();
    uploadData.append('title', title);
    uploadData.append('cover', cover, cover.name);
    
    fetch('http://127.0.0.1:8000/books/', {
      method: 'POST',
      body: uploadData
    })
    .then( res => console.log(res))
    .catch(error => console.log(error))
    
    setfile("")
    setdownload("Download");
  }
  const downloadhtml = () => {
    setdownload("Download");
    const link = title+'.html';
    fetch(link).then(response => {
      response.blob().then(blob => {
          // Creating new object of PDF file
          const fileURL = window.URL.createObjectURL(blob);
          // Setting various property values
          let alink = document.createElement('a');
          alink.href = fileURL;
          alink.download = link;
          alink.click();
      })
  })
  }
  const [preview, setPreview] = useState(null);

  const fileHandler = evt => {
     setCever(evt.target.files[0])
      const f = evt.target.files[0];

      if (f) {
          const reader = new FileReader();
          reader.onload = ({ target: { result } }) => {
              setPreview(result);
          };

          reader.readAsDataURL(f); // you can read image file as DataURL like this.
      } else {
          setPreview(null);
      }
  };


  return (
    <div className="App">
      <div className="text">
      
      <h1>Upload your Design</h1>
      <p>Transform any hand-drawn design into Html Code.</p>
      <div className='yours'>
      <label className='title'>
        Name for your File:
        <input type="text" value={title} onChange={(evt) => setTitle(evt.target.value)}/>
      </label>
      <br/>
      <label className='image'>
        Image:
        {/* <input type="file" onChange={(evt) => setCever(evt.target.files[0])}/>
        <img src={file} width="100px" height="auto"/> */}
        <input
               type="file"
               accept="image/*"
               onChange={fileHandler}
            />
            { preview && <img src={preview} width="250px" height="auto" /> }
        
      </label>
      <br/>
      { file === "" ? <div></div> : <button className='upload' onClick={() => newBook()}>{file}</button>}
      
      {download === "" ? <div></div>:
      <button className='upload' onClick={() => downloadhtml()}>{download}</button>}
      </div></div>
    </div>
  );
}

export default App;
