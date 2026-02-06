import React from 'react';

interface ErrorMessageProps {
  message: string;
  isVisible: boolean;
  onDismiss?: () => void;
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({
  message,
  isVisible,
  onDismiss
}) => {
  if (!isVisible) {
    return null;
  }

  return (
    <div className="error-message-container">
      <div className="error-message">
        <span className="error-text">{message}</span>
        {onDismiss && (
          <button className="dismiss-button" onClick={onDismiss}>
            ×
          </button>
        )}
      </div>
    </div>
  );
};

export default ErrorMessage;