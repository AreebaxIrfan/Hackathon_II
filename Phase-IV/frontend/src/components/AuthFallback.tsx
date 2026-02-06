import React from 'react';

interface AuthFallbackProps {
  onRetry?: () => void;
  message?: string;
}

export const AuthFallback: React.FC<AuthFallbackProps> = ({
  onRetry,
  message = "Authentication is required to use this feature. Please try again."
}) => {
  return (
    <div className="auth-fallback-container">
      <div className="auth-fallback-content">
        <h3>Authentication Required</h3>
        <p>{message}</p>
        {onRetry && (
          <button onClick={onRetry} className="retry-button">
            Retry Authentication
          </button>
        )}
      </div>
    </div>
  );
};

export default AuthFallback;