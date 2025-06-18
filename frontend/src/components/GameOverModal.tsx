import React from 'react';

interface GameOverModalProps {
  isOpen: boolean;
  won: boolean;
  guessCount: number;
  onRestart: () => void;
}

export const GameOverModal: React.FC<GameOverModalProps> = ({ isOpen, won, guessCount, onRestart }) => {
  if (!isOpen) return null;

  return (
    <div className="gameover-modal-overlay">
      <div className="gameover-modal">
        <h2 className="modal-title">STATISTICS</h2>
        <div className="modal-stats">
          <div>
            <div className="modal-stat-value">1</div>
            <div className="modal-stat-label">Played</div>
          </div>
          <div>
            <div className="modal-stat-value">{won ? 100 : 0}</div>
            <div className="modal-stat-label">Win %</div>
          </div>
          <div>
            <div className="modal-stat-value">{won ? 1 : 0}</div>
            <div className="modal-stat-label">Current Streak</div>
          </div>
          <div>
            <div className="modal-stat-value">{won ? 1 : 0}</div>
            <div className="modal-stat-label">Max Streak</div>
          </div>
        </div>
        <div className="modal-guess-dist">
          <div className="modal-guess-title">GUESS DISTRIBUTION</div>
          <div className="modal-guess-bars">
            {[1,2,3,4,5,6].map(n => (
              <div key={n} className="modal-guess-bar-row">
                <span className="modal-guess-bar-label">{n}</span>
                <span className={`modal-guess-bar ${guessCount === n ? 'modal-guess-bar-active' : ''}`}>{guessCount === n ? 1 : 0}</span>
              </div>
            ))}
          </div>
        </div>
        <div className="modal-actions">
          <button className="modal-btn modal-btn-play" onClick={onRestart}>PLAY AGAIN!</button>
        </div>
      </div>
    </div>
  );
};
