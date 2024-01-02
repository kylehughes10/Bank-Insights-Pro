import React, { useState } from 'react';
import './PricingPage.css'; // Make sure to create a corresponding CSS file
import PaymentModal from './PaymentModal'; // Make sure this imports the PaymentModal component correctly
import Explorer from './imgs/explorer-icon.svg'
import Analyst from './imgs/analsyt-icon.svg'
import Executive from './imgs/executive-icon.svg'

function PricingPage() {
  const [showModal, setShowModal] = useState(false);
  const [selectedPlan, setSelectedPlan] = useState({ name: '', price: '' });

  const openModal = (planName, planPrice) => {
    setSelectedPlan({ name: planName, price: planPrice });
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
  };

  return (
    <div className="pricing-container">
      <h1>Choose Your Plan</h1>
      <div className="pricing-options">
        <div className="pricing-option">
          <img src={Explorer} alt="Bank Insights Pro Logo" className="plan-logo" />
          <h2>Explorer</h2>
          <p className="price">$10</p>
          <ul>
            <li>Access to One Detailed Bank Report</li>
            <li>Structured UBPR Data for In-Depth Analysis</li>
            <li>Email Support</li>
          </ul>
          <button onClick={() => openModal('Explorer', '$10')}>Get Report</button>
          <p className="small">Ideal for individual researchers and investors.</p>
        </div>
        <div className="pricing-option">
          <img src={Analyst} alt="Bank Insights Pro Logo" className="plan-logo" />
          <h2>Analyst</h2>
          <p className="price">$30</p>
          <ul>
            <li>5 Comprehensive Report Pulls</li>
            <li>Ability to Compare Metrics Across 5 Banks</li>
            <li>Priority Email Support</li>
          </ul>
          <button onClick={() => openModal('Analyst', '$30')}>Get Reports</button>
          <p className="small">Perfect for professionals needing broader banking insights.</p>
        </div>
        <div className="pricing-option">
          <img src={Executive} alt="Bank Insights Pro Logo" className="plan-logo" />
          <h2>Executive</h2>
          <p className="price">$50/mo</p>
          <ul>
            <li>Unlimited Access to All Bank Data</li>
            <li>Unlimited Reports with Advanced Comparisons</li>
            <li>Premium Support and Consultation</li>
          </ul>
          <button onClick={() => openModal('Executive', '$50/mo')}>Subscribe</button>
          {/* <p className='user-account'>Already have an account?</p> */}
          <p className="small">Designed for organizations seeking comprehensive data and analysis.</p>
        </div>
      </div>
      {showModal && <PaymentModal selectedPlan={selectedPlan} onClose={closeModal} />}
    </div>
  );
}

export default PricingPage;
