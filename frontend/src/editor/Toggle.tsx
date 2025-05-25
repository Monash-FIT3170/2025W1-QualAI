// Toggle.tsx
import React from 'react';

interface ToggleProps {
  children: React.ReactNode;
  pressed: boolean;
  onPressedChange: () => void;
  className?: string;
}

export const Toggle: React.FC<ToggleProps> = ({
  children,
  pressed,
  onPressedChange,
  className = '',
}) => {
  return (
    <button
      type="button"
      className={`
        inline-flex items-center justify-center rounded-md px-2 py-1 text-sm 
        transition-colors hover:bg-gray-200
        ${pressed ? 'bg-gray-200 text-gray-900' : 'bg-transparent text-gray-700'}
        ${className}
      `}
      onClick={onPressedChange}
      data-state={pressed ? 'on' : 'off'}
      aria-pressed={pressed}
    >
      {children}
    </button>
  );
};

export default Toggle;