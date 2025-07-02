import { createRoot } from 'react-dom/client';
import './style/tailwind.css';
import './style/app.css';

import RootApp from './RootApp';

const root = createRoot(document.getElementById('root') as HTMLElement);
root.render(<RootApp />);
