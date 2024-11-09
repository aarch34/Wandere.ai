
import styles from './loading.module.css';

export default function Loading() {
  return (
    <div className={styles.loaderContainer}>
      <img src="/airplane-svgrepo-com.svg" alt="Plane icon" className={styles.plane} />
    </div>
  );
}
