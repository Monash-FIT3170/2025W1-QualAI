import React from 'react';

interface ToggleProps {
  children: React.ReactNode;
  pressed: boolean;
  onPressedChange: () => void; // Note: original was (pressed: boolean) => void, if it's just a toggle, () => void is fine.
                              // If you need the new state back, it should be (newState: boolean) => void
  className?: string;
  disabled?: boolean; // Added
  title?: string;     // Added
}

export const Toggle: React.FC<ToggleProps> = ({
  children,
  pressed,
  onPressedChange,
  className = '',
  disabled = false, // Added default value
  title,            // Added
}) => {
  return (
    <button
      type="button"
      className={`
        inline-flex items-center justify-center rounded-md px-2 py-1 text-sm 
        transition-colors hover:bg-gray-200 dark:hover:bg-slate-700
        focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring
        disabled:pointer-events-none disabled:opacity-50
        ${pressed ? 'bg-gray-200 text-gray-900 dark:bg-slate-700 dark:text-slate-100' : 'bg-transparent text-gray-700 dark:text-slate-300'}
        ${className}
      `}
      onClick={onPressedChange}
      data-state={pressed ? 'on' : 'off'}
      aria-pressed={pressed}
      disabled={disabled} // Use the disabled prop
      title={title}       // Use the title prop
    >
      {children}
    </button>
  );
};

export default Toggle;