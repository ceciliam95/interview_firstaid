import React from 'react';
import './page_header.css';

const PageHeader = () => {
   return (
      <div class = 'header'>
         <h2>
           <span class = "header-link"> Home </span>
           <span class = "header-link"> About Us </span>
           <span class = "header-link"> <a href = "pricing.html"> Pricing </a> </span>
           <span class = "header-link"> <a href = "signup.html"> Sign Up </a> </span>
           <span class = "header-link"> Login </span>
         </h2>

      </div>
   );
};

export default PageHeader;