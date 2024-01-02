import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './PaymentModal.css';

function PaymentModal({ selectedPlan, onClose }) {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState('paymentDetails');
  const [paymentDetails, setPaymentDetails] = useState({
    nameOnCard: '',
    cardNumber: '',
    expiryMonth: '',
    expiryYear: '',
    cvv: '',
    promoCode: ''
  });
  const [email, setEmail] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setPaymentDetails(prevDetails => ({
      ...prevDetails,
      [name]: value
    }));
  };

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handlePaymentSubmit = (e) => {
    e.preventDefault();
    setCurrentStep('emailEntry');
  };

  const handleEmailSubmit = (e) => {
    e.preventDefault();
    navigate('/reports'); // Use navigate to redirect to the reports page
  };

  return (
    <div className="payment-modal">
      <div className="modal-content">
        <span className="close-button" onClick={onClose}>&times;</span>
        <h2>{currentStep === 'paymentDetails' ? `Selected Plan: ${selectedPlan.name} ${selectedPlan.price}` : 'Thank You!'}</h2>
        {currentStep === 'paymentDetails' && (
          <form onSubmit={handlePaymentSubmit}>
            <div className="payment-methods">
            </div>
            <input
              type="text"
              name="nameOnCard"
              placeholder="Name on Card"
              value={paymentDetails.nameOnCard}
              onChange={handleInputChange}
              required
            />
            <input
              type="text"
              name="cardNumber"
              placeholder="Card Number"
              value={paymentDetails.cardNumber}
              onChange={handleInputChange}
              required
            />
            <div className="expiry-cvv">
              <input
                type="text"
                name="expiryMonth"
                placeholder="MM"
                value={paymentDetails.expiryMonth}
                onChange={handleInputChange}
                required
              />
              <input
                type="text"
                name="expiryYear"
                placeholder="YYYY"
                value={paymentDetails.expiryYear}
                onChange={handleInputChange}
                required
              />
              <input
                type="text"
                name="cvv"
                placeholder="CVV"
                value={paymentDetails.cvv}
                onChange={handleInputChange}
                required
              />
            </div>
            <input
              type="text"
              name="promoCode"
              placeholder="Promo Code"
              value={paymentDetails.promoCode}
              onChange={handleInputChange}
            />
            <button type="submit" className="submit-button">Let's Go!</button>
          </form>
        )}
        {currentStep === 'emailEntry' && (
          <form onSubmit={handleEmailSubmit}>
            <p>Where should we send you reports? Just enter your email address below.</p>
            <input
              type="email"
              name="email"
              placeholder="Email Address"
              value={email}
              onChange={handleEmailChange}
              required
            />
            <button type="submit" className="submit-button">Continue</button>
          </form>
        )}
      </div>
    </div>
  );
}

export default PaymentModal;
