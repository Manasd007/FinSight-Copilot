export default function Taskbar({ onNewChat, onToggleTheme, theme }: {
  onNewChat: () => void;
  onToggleTheme: () => void;
  theme: 'light' | 'dark';
}) {
  return (
    <header
  style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '100%', position: 'sticky', top: 0, zIndex: 50 }}
  className="px-6 py-3 bg-white dark:bg-gray-900 shadow-sm border-b border-gray-200 dark:border-gray-800"
>
      {/* Left: Menu + New Chat + Divider + Logo */}
      <div className="flex items-center gap-4">
        <button className="text-2xl p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-800" title="Menu">
          <span role="img" aria-label="menu">☰</span>
        </button>
        <button
          className="ml-1 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 font-medium transition"
          onClick={onNewChat}
        >
          New Chat
        </button>
        <div className="mx-4 h-6 w-px bg-gray-300 dark:bg-gray-700" />
        <span className="text-xl font-bold tracking-wide text-blue-800 dark:text-blue-200 flex items-center gap-2">
          <span role="img" aria-label="logo">💹</span> Finsight Copilot
        </span>
      </div>
      {/* Right: Theme toggle + Profile */}
      <div className="flex items-center gap-4">
        <button
          className="p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-800"
          onClick={onToggleTheme}
          title="Toggle light/dark mode"
        >
          {theme === 'light' ? '🌞' : '🌙'}
        </button>
        <button className="w-9 h-9 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center text-lg font-bold text-blue-800 dark:text-blue-200">
          <span role="img" aria-label="profile">👤</span>
        </button>
      </div>
    </header>
  );
}