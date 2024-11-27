import { Link } from 'react-router-dom';

export default function About() {
  return (
    <div>
      <nav>
        <Link to="/">Home</Link> | <Link to="/about">About</Link>
      </nav>
      <h1>Welcome to the About Page</h1>
    </div>
  );
}
