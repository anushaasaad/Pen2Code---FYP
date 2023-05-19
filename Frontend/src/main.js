import React from "react";
import './Main.css';
import Header from './Header.js';
import App from './App.js';
import Content from './content.js';
import Footer from './footer.js';
import 'bootstrap/dist/css/bootstrap.css';
import Slide1 from './slide.png';
import Slider from './slider.js';
function Main() {
  return (
    <div class="hero">
      <Header />
    <div className="main">
        <div className="maxwidth">
            <div className="box">
                <h2>Pen2Code</h2>
                <p>An AI-based web application to write boilerplate code. Converts hand-drawn mockup images into HTML webpages.</p>
            </div>
            <div className="button">
              <p><a href="#">Try out Pen2Code</a> </p>
              </div>
            
        </div>
        <Content />
        <Slider />
        <App />
        <Footer />
        </div>
     </div>
  );
}

export default Main;
