import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';
import './App.css';
import PricingPage from './PricingPage';
import SignUpPage from './SignUpPage';
import Reports from './reports';
import heroImage from './imgs/heroimg2.jpg';
import logo from './imgs/logo2.png';
import chaseLogo from './imgs/chasebanklogo.png';
import firstUnitedLogo from './imgs/fublogo.jpg';
import simmonsBankLogo from './imgs/simmonsbanklogo.png';

function App() {
  const [fdicCertNumber, setFdicCertNumber] = useState('');
  const [loading, setLoading] = useState(false);
  const [reportContent, setReportContent] = useState('');

  const generateReport = () => {
    if (!fdicCertNumber) {
      alert('Please enter an FDIC Certificate Number.');
      return;
    }
    setLoading(true);
    setTimeout(() => {
      setReportContent('Simulated report content for FDIC Cert Number: ' + fdicCertNumber);
      setLoading(false);
    }, 3000);
  };

  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <Logo /> {/* Updated to use the Logo component */}
          <ul className="Navigation-list">
            {/* <li><a href="#services">Services</a></li>
            <li><a href="#learn-more">Learn More</a></li>
            <li><a href="#resources">Resources</a></li> */}
            <SubscribeButton />
          </ul>
        </header>
        <Routes>
          <Route exact path="/" element={
            <>
              <HeroSection generateReport={generateReport} />
              <TrustedBanks />
              <main>
                {/* ... */}
              </main>
            </>
          } />
          <Route path="/pricing" element={<PricingPage />} />
          <Route path="/reports" element={<Reports />} />
          <Route path="/signup" element={<SignUpPage />} />
        </Routes>
      </div>
    </Router>
  );
}

function Logo() {
  const navigate = useNavigate();
  return (
    <img src={logo} alt="Bank Insights Pro Logo" className="App-logo" onClick={() => navigate('/')} />
  );
}

function SubscribeButton() {
  const navigate = useNavigate();
  return (
    <button className="Subscribe-button" onClick={() => navigate('/signup')}>
      Sign Up
    </button>
  );
}

function HeroSection({ generateReport }) {
  const navigate = useNavigate();
  return (
    <section className="Hero-section">
      <div className="Hero-content">
        <h1>BANK PERFORMANCE REPORT PORTAL</h1>
        <p>Unlock the full potential of FFIEC's UBPR with our intuitive platform. Effortlessly access structured, analytical reports on commercial bank performance and financials. Choose flexibility with pay-per-report or embrace unlimited insights with our monthly subscription. Simplify your investment decisions — only at BankInsightsPro.</p>
        <div className="Start-button-container">
          <button className="Start-button" onClick={() => navigate('/pricing')}>Generate Report</button>
        </div>
      </div>
      <div className='heroImgDiv'>
        <img src={heroImage} alt="Bank Performance Report Portal" className="Hero-image" />
      </div>
    </section>
  );
}

function TrustedBanks() {
  return (
    <div className="Trusted-banks">
      <p className="Trusted-text">Trusted by</p>
      <div className="Bank-logos">
        <img src={chaseLogo} alt="Chase Logo" className="Bank-logo" />
        <img src={firstUnitedLogo} alt="First United Logo" className="Bank-logo" />
        <img src={simmonsBankLogo} alt="Simmons Bank Logo" className="Bank-logo" />
      </div>
    </div>
  );
}

export default App;
