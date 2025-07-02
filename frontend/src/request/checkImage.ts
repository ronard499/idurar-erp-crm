import axios from 'axios';
import { BASE_URL } from '@/config/serverApiConfig';

/**
 * Check if an image exists at the given path
 * @param path - URL path to the image
 * @returns Promise resolving to true if image exists, false otherwise
 */
export default async function checkImage(path: string): Promise<boolean> {
  const result = await axios
    .get(path, {
      headers: {
        'Access-Control-Allow-Origin': BASE_URL,
      },
    })
    .then((response) => {
      if (response.status === 200) return true;
      else return false;
    })
    .catch(() => {
      return false;
    });

  return result;
}
