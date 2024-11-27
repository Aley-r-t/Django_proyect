import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <div>
      <nav>
        <Link to="/">Home</Link> | <Link to="/about">About</Link>
      </nav>
      <h1>Welcome to the Home Page</h1>
    </div>
  );
}
