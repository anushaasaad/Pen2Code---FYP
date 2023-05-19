import React from "react";
import './header.css';
import Logo from './logo.PNG';
function Header() {
  return (
       <nav class="navbar">
		<div class="max-width">
            <div className="Left">
                <img src={Logo}/>
            </div>
			<ul class="menu">
				<li><a href="#">Services</a></li>
				<li><a href="#">About us</a></li>
				<li><a href="#">Packages</a></li>
				<li><a href="#">FAQ's</a></li>
			</ul>
			<div class="menu-btn">
				<i class="fas fa-bars">

				</i>
			</div>
		</div>
	</nav> 
  );
}

export default Header;
