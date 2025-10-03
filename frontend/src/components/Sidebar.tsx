import logoUrl from '../assets/logoSidebar.svg';
import type { Conversation } from "../types";


interface Props {
    conversations: Conversation[];
    onNewConversation: () => void;
    onSelectConversation: (id: number) => void;
    collapsed: boolean; // controlled
    setCollapsed: (v: boolean) => void;
    selectedId?: number | null;
}


export default function Sidebar({ conversations, onNewConversation, onSelectConversation, collapsed, setCollapsed, selectedId }: Props) {
    return (
        // outer group to allow hover expansion when collapsed
        <div className={`group relative h-screen z-20`}>
            <aside
                className={`bg-white border-r shadow-sm h-full transition-all duration-400 ease-in-out ${collapsed ? "w-16" : "w-64"
                    }`}
            >
                <div className="flex items-center justify-between px-3 py-2">
                    <div className="flex items-center gap-2" onClick={() => setCollapsed(false)}>
                        <img src={logoUrl} alt="logo" className="w-8 h-8 ml-1" />

                    </div>
                    {/* {!collapsed && <div className="font-semibold transition-all duration-1000 ease-in-out">My AI Chat</div>} */}
                    <div>
                        {!collapsed && (
                            <button onClick={() => setCollapsed(true)} className="rounded hover:bg-slate-100">⏴</button>
                        )
                            // <button onClick={() => setCollapsed(false)} className="p-1 rounded hover:bg-slate-100">⏵</button>
                        }
                    </div>
                </div>


                <div className="p-3">
                    <button onClick={onNewConversation} className="w-full flex items-center gap-3 px-3 py-2 bg-blue-600 text-white rounded hover:opacity-95">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" /></svg>
                        {!collapsed && <span>New conversation</span>}
                    </button>
                </div>


                <div className="px-3 py-2 text-xs text-slate-500">History</div>
                <div className="overflow-auto px-2" style={{ maxHeight: 'calc(100vh - 160px)' }}>
                    <ul className="space-y-1">
                        {conversations.map((c) => (
                            <li key={c.id}>
                                <button
                                    onClick={() => onSelectConversation(c.id)}
                                    className={`w-full text-left flex items-center gap-3 px-2 py-2 rounded ${selectedId === c.id ? 'bg-slate-100' : 'hover:bg-slate-50'}`}
                                >
                                    <div className="flex-1 overflow-hidden">
                                        <div className="text-sm truncate">{c.title || `Conversation ${c.id}`}</div>
                                        {!collapsed && <div className="text-xs text-slate-400">{c.created_at ? new Date(c.created_at).toLocaleString() : `#${c.id}`}</div>}
                                    </div>
                                    {!collapsed && <div className="text-slate-400">›</div>}
                                </button>
                            </li>
                        ))}
                    </ul>
                </div>
            </aside>
        </div>
    );
}
