import logoUrl from '../assets/logoHeader.svg';

interface HeaderProps {
    modelName?: string;
    logoUrl?: string;
    title?: string;
    onToggleSidebar?: () => void;
}


export default function Header({
    modelName = "openai/gpt-oss-20b",
    title = "",
    onToggleSidebar,
}: HeaderProps) {
    return (
        <header className="w-full flex items-center justify-between px-4 py-3 bg-white border-b relative">
            {/* left: model name */}
            <div className="flex items-center gap-3">
                <div className="text-sm text-slate-500">{modelName}</div>
            </div>


            {/* center: logo */}
            <div className="flex-1 flex items-center justify-center">
                <img src={logoUrl} alt="logo" className="w-auto" />
            </div>


            {/* right: conversation title + toggle button */}
            <div className="flex items-center gap-3">
                <div className="text-sm font-medium text-slate-700 truncate max-w-xs">{title || "No conversation selected"}</div>
                {onToggleSidebar && (
                    <button onClick={onToggleSidebar} className="p-1 rounded hover:bg-slate-100">
                        ☰
                    </button>
                )}
            </div>
        </header>
    );
}
