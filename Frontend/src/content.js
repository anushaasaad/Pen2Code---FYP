import React from "react";
import './Main.css';
import Pic from './p2c.jpg';
function Content() {
  return (
    <div className="Content">
        <div className="outer">
          <div className="left">
            <img src={Pic} />
            </div>
          <div className="right">
            <div className="text">
              <p>Pen2code will take hand-drawn mockup images as input and produce an HTML file as output containing the UI code. <br/>
              Bridge the gap that exists otherwise between the stakeholder’s vision and the coder/developer</p>
            </div>
            <div className="Btn">
              <span>Convert yours</span>
              </div>
          </div>
        </div>
     </div>
  );
}

export default Content;
