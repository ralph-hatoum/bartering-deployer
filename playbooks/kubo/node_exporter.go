package main

import (
	"os"
	"os/exec"
	"path/filepath"
)

func main() {

	PORT := 9100

	args := os.Args[1:]

	nodeName := args[0]

}

func getFolderSize(path string) (int64, error) {
	var size int64
	err := filepath.Walk(path, func(_ string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if !info.IsDir() {
			size += info.Size()
		}
		return nil
	})
	if err != nil {
		return 0, err
	}
	return size, nil
}

func listPinnedCid() (string, error) {
	args := []string{"pin", "ls"}
	cmd := exec.Command("ipfs", args...)
	output, err := cmd.CombinedOutput()
	if err != nil {
		return "", err
	}

}
