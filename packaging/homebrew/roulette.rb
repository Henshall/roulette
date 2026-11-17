# Homebrew formula for roulette. The published copy lives in the tap repo
# (github.com/Henshall/homebrew-tap, Formula/roulette.rb); keep the two in sync.
# On each release: update `url` to the new tag and `sha256` to the checksum of
# that tarball (curl -fsSL <url> | shasum -a 256).
class Roulette < Formula
  desc "Zero-edge roulette table for the terminal, with a croupier you can bribe"
  homepage "https://github.com/Henshall/roulette"
  url "https://github.com/Henshall/roulette/archive/refs/tags/v2.6.0.tar.gz"
  sha256 "3b21cdc0df272ac7652dd7e5c23de182ef8421ecea86dbfede47d4f8693b281f"
  license "MIT"

  # A single standard-library Python 3 script. It runs on the python3 that
  # ships with Apple's Command Line Tools (which Homebrew already requires).

  def install
    bin.install "roulette"
    man1.install "man/roulette.1"
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/roulette --version")
    ENV["HOME"] = testpath
    assert_match "R O U L E T T E", shell_output("#{bin}/roulette --stats")
    system bin/"roulette", "--spin", "--no-color"
  end
end
