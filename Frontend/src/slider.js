import React, { useState } from 'react';
import './App.css';
import '../node_modules/bootstrap/dist/css/bootstrap.css';
import Pic1 from './Samples/1.png';
import Pic2 from './Samples/2.png';
import Pic3 from './Samples/3.png';
import {Routes, Route, useNavigate} from 'react-router-dom';
import { BrowserRouter } from 'react-router-dom';
function App() {
    const [ title, setTitle ] = useState("");
    const [ link, setlink ] = useState("");
    const pic1 = () => {
            setTitle("download");
            setlink("1.html")
        }
    const pic2 = () => {
        setTitle("download");
        setlink("2.html")
    }
    const pic3 = () => {
        setTitle("download");
        setlink("3.html")
    }
    const Download = () => {{
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
        }}
  return (
    <div className='slider'>
		<h1><span className="font-weight: 600;">USE THESE SAMPLES</span> </h1>
			<div className="servcontent" >
				<div className="card">
					<div className="box">
						<img src={Pic1} />
                        <button onClick={pic1}>use this</button>
					</div>
				</div>
				<div className="card">
					<div className="box">
						<img src={Pic2} />
                        <button onClick={pic2}>Use this</button>
					</div>
				</div>
				<div className="card">
					<div className="box">
						<img src={Pic3} />
                        <button onClick={pic3}>Use this</button>
					</div>
				</div>
                <div>
                <button onClick={Download}>{title}</button>
             </div>
        </div></div>
    
  );
}

export default App;
