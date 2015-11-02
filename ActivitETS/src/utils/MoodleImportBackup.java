package utils;


import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;
import org.apache.commons.io.IOUtils;

public class MoodleImportBackup {
	
	public static void compress(File extractedMoodleBackup,
			File destMoodleBackupMbzFile) {

		validateInputParams(extractedMoodleBackup, destMoodleBackupMbzFile);

		ZipOutputStream zip = null;
		FileOutputStream fileWriter = null;
		try {
			fileWriter = new FileOutputStream(destMoodleBackupMbzFile);
			zip = new ZipOutputStream(fileWriter);
			for (File backupFile : extractedMoodleBackup.listFiles()) {
				addFileToZip("", backupFile, zip);
			}
			zip.flush();
		} catch (Exception e) {
			//throw new MoodleBackupExporterException(e);
		} finally {
			IOUtils.closeQuietly(zip);
		}
	}

	private static void addFileToZip(String path, File folder,
			ZipOutputStream zip) throws Exception {
		if (folder.isDirectory()) {
			addFolderToZip(path, folder, zip);
		} else {
			byte[] buf = new byte[1024];
			int len;
			FileInputStream in = new FileInputStream(folder.toString());
			zip.putNextEntry(new ZipEntry(path + "/" + folder.getName()));
			while ((len = in.read(buf)) > 0) {
				zip.write(buf, 0, len);
			}
		}
	}

	private static void addFolderToZip(String path, File folder,
			ZipOutputStream zip) throws Exception {
		for (String fileName : folder.list()) {
			if (path.equals("")) {
				addFileToZip(folder.getName(), new File(folder, fileName), zip);
			} else {
				addFileToZip(path + "/" + folder.getName(), new File(folder,
						fileName), zip);
			}
		}
	}

	private static void validateInputParams(File extractedMoodleBackup,
			File destMoodleBackupMbzFile) {
		if (extractedMoodleBackup == null || !extractedMoodleBackup.exists()
				|| !extractedMoodleBackup.isDirectory()) {
			throw new IllegalArgumentException(
					"Given moodle backup folder is invalid");
		}
		if (destMoodleBackupMbzFile == null) {
			throw new IllegalArgumentException("Final mbz file cannot be null");
		}
	}
}
